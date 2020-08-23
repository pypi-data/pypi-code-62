import warnings
from typing import Optional

import numpy as np
import pandas as pd
from scipy.sparse import issparse
from anndata import AnnData

from ... import logging as logg
from .._distributed import materialize_as_ndarray
from .._utils import _get_mean_var
from ..._compat import Literal


def filter_features_dispersion(
    data: AnnData,
    flavor: Literal['seurat', 'cell_ranger'] = 'seurat',
    min_disp: Optional[float] = None,
    max_disp: Optional[float] = None,
    min_mean: Optional[float] = None,
    max_mean: Optional[float] = None,
    n_bins: int = 20,
    n_top_features: Optional[int] = None,
    log: bool = True,
    subset: bool = True,
    copy: bool = False,
):
    """\
    Extract highly variable features [Satija15]_ [Zheng17]_.
    .. warning::
        .. deprecated:: 1.3.6
            Use :func:`~scanpy.pp.highly_variable_features`
            instead. The new function is equivalent to the present
            function, except that
            * the new function always expects logarithmized data
            * `subset=False` in the new function, it suffices to
              merely annotate the features, tools like `pp.pca` will
              detect the annotation
            * you can now call: `sc.pl.highly_variable_features(adata)`
            * `copy` is replaced by `inplace`
    If trying out parameters, pass the data matrix instead of AnnData.
    Depending on `flavor`, this reproduces the R-implementations of Seurat
    [Satija15]_ and Cell Ranger [Zheng17]_.
    The normalized dispersion is obtained by scaling with the mean and standard
    deviation of the dispersions for features falling into a given bin for mean
    expression of features. This means that for each bin of mean expression, highly
    variable features are selected.
    Use `flavor='cell_ranger'` with care and in the same way as in
    :func:`~scanpy.pp.recipe_zheng17`.
    Parameters
    ----------
    data
        The (annotated) data matrix of shape `n_obs` × `n_vars`. Rows correspond
        to subjects and columns to features.
    flavor
        Choose the flavor for computing normalized dispersion. If choosing
        'seurat', this expects non-logarithmized data – the logarithm of mean
        and dispersion is taken internally when `log` is at its default value
        `True`. For 'cell_ranger', this is usually called for logarithmized data
        – in this case you should set `log` to `False`. In their default
        workflows, Seurat passes the cutoffs whereas Cell Ranger passes
        `n_top_features`.
    min_mean
    max_mean
    min_disp
    max_disp
        If `n_top_features` unequals `None`, these cutoffs for the means and the
        normalized dispersions are ignored.
    n_bins
        Number of bins for binning the mean feature expression. Normalization is
        done with respect to each bin. If just a single feature falls into a bin,
        the normalized dispersion is artificially set to 1. You'll be informed
        about this if you set `settings.verbosity = 4`.
    n_top_features
        Number of highly-variable features to keep.
    log
        Use the logarithm of the mean to variance ratio.
    subset
        Keep highly-variable features only (if True) else write a bool array for h
        ighly-variable features while keeping all features
    copy
        If an :class:`~anndata.AnnData` is passed, determines whether a copy
        is returned.
    Returns
    -------
    If an AnnData `adata` is passed, returns or updates `adata` depending on
    `copy`. It filters the `adata` and adds the annotations
    **means** : adata.var
        Means per feature. Logarithmized when `log` is `True`.
    **dispersions** : adata.var
        Dispersions per feature. Logarithmized when `log` is `True`.
    **dispersions_norm** : adata.var
        Normalized dispersions per feature. Logarithmized when `log` is `True`.
    If a data matrix `X` is passed, the annotation is returned as `np.recarray`
    with the same information stored in fields: `feature_subset`, `means`, `dispersions`, `dispersion_norm`.
    """
    if (
        n_top_features is not None
        and not all(x is None for x in [min_disp, max_disp, min_mean, max_mean])
    ):
        logg.info('If you pass `n_top_features`, all cutoffs are ignored.')
    if min_disp is None: min_disp = 0.5
    if min_mean is None: min_mean = 0.0125
    if max_mean is None: max_mean = 3
    if isinstance(data, AnnData):
        adata = data.copy() if copy else data
        result = filter_features_dispersion(
            adata.X,
            log=log,
            min_disp=min_disp, max_disp=max_disp,
            min_mean=min_mean, max_mean=max_mean,
            n_top_features=n_top_features,
            flavor=flavor,
        )
        adata.var['means'] = result['means']
        adata.var['dispersions'] = result['dispersions']
        adata.var['dispersions_norm'] = result['dispersions_norm']
        if subset:
            adata._inplace_subset_var(result['feature_subset'])
        else:
            adata.var['highly_variable'] = result['feature_subset']
        return adata if copy else None
    start = logg.info('extracting highly variable features')
    X = data  # no copy necessary, X remains unchanged in the following
    mean, var = materialize_as_ndarray(_get_mean_var(X))
    # now actually compute the dispersion
    mean[mean == 0] = 1e-12  # set entries equal to zero to small value
    dispersion = var / mean
    if log:  # logarithmized mean as in Seurat
        dispersion[dispersion == 0] = np.nan
        dispersion = np.log(dispersion)
        mean = np.log1p(mean)
    # all of the following quantities are "per-feature" here
    df = pd.DataFrame()
    df['mean'] = mean
    df['dispersion'] = dispersion
    if flavor == 'seurat':
        df['mean_bin'] = pd.cut(df['mean'], bins=n_bins)
        disp_grouped = df.groupby('mean_bin')['dispersion']
        disp_mean_bin = disp_grouped.mean()
        disp_std_bin = disp_grouped.std(ddof=1)
        # retrieve those features that have nan std, these are the ones where
        # only a single feature fell in the bin and implicitly set them to have
        # a normalized disperion of 1
        one_feature_per_bin = disp_std_bin.isnull()
        gen_indices = np.where(one_feature_per_bin[df['mean_bin'].values])[0].tolist()
        if len(gen_indices) > 0:
            logg.debug(
                f'feature indices {gen_indices} fell into a single bin: their '
                'normalized dispersion was set to 1.\n    '
                'Decreasing `n_bins` will likely avoid this effect.'
            )
        # Circumvent pandas 0.23 bug. Both sides of the assignment have dtype==float32,
        # but there’s still a dtype error without “.value”.
        disp_std_bin[one_feature_per_bin] = disp_mean_bin[one_feature_per_bin.values].values
        disp_mean_bin[one_feature_per_bin] = 0
        # actually do the normalization
        df['dispersion_norm'] = (
            df['dispersion'].values  # use values here as index differs
            - disp_mean_bin[df['mean_bin'].values].values
        ) / disp_std_bin[df['mean_bin'].values].values
    elif flavor == 'cell_ranger':
        from statsmodels import robust
        df['mean_bin'] = pd.cut(df['mean'], np.r_[-np.inf,
            np.percentile(df['mean'], np.arange(10, 105, 5)), np.inf])
        disp_grouped = df.groupby('mean_bin')['dispersion']
        disp_median_bin = disp_grouped.median()
        # the next line raises the warning: "Mean of empty slice"
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            disp_mad_bin = disp_grouped.apply(robust.mad)
        df['dispersion_norm'] = np.abs((
            df['dispersion'].values
            - disp_median_bin[df['mean_bin'].values].values
        )) / disp_mad_bin[df['mean_bin'].values].values
    else:
        raise ValueError('`flavor` needs to be "seurat" or "cell_ranger"')
    dispersion_norm = df['dispersion_norm'].values.astype('float32')
    if n_top_features is not None:
        dispersion_norm = dispersion_norm[~np.isnan(dispersion_norm)]
        dispersion_norm[::-1].sort()  # interestingly, np.argpartition is slightly slower
        disp_cut_off = dispersion_norm[n_top_features-1]
        feature_subset = df['dispersion_norm'].values >= disp_cut_off
        logg.debug(
            f'the {n_top_features} top features correspond to a '
            f'normalized dispersion cutoff of {disp_cut_off}'
        )
    else:
        max_disp = np.inf if max_disp is None else max_disp
        dispersion_norm[np.isnan(dispersion_norm)] = 0  # similar to Seurat
        feature_subset = np.logical_and.reduce((
            mean > min_mean,
            mean < max_mean,
            dispersion_norm > min_disp,
            dispersion_norm < max_disp,
        ))
    logg.info('    finished', time=start)
    return np.rec.fromarrays((
        feature_subset,
        df['mean'].values,
        df['dispersion'].values,
        df['dispersion_norm'].values.astype('float32', copy=False),
    ), dtype=[
        ('feature_subset', bool),
        ('means', 'float32'),
        ('dispersions', 'float32'),
        ('dispersions_norm', 'float32'),
    ])


def filter_features_cv_deprecated(X, Ecutoff, cvFilter):
    """ Filter features by coefficient of variance and mean."""
    return _filter_features(X, Ecutoff, cvFilter, np.std)


def filter_features_fano_deprecated(X, Ecutoff, Vcutoff):
    """Filter features by fano factor and mean."""
    return _filter_features(X, Ecutoff, Vcutoff, np.var)


def _filter_features(X, e_cutoff, v_cutoff, meth):
    """\
    See `filter_features_dispersion`.
    Reference: Weinreb et al. (2017)."""
    if issparse(X):
        raise ValueError('Not defined for sparse input. See `filter_features_dispersion`.')
    mean_filter = np.mean(X, axis=0) > e_cutoff
    var_filter = meth(X, axis=0) / (np.mean(X, axis=0) + .0001) > v_cutoff
    feature_subset = np.nonzero(np.all([mean_filter, var_filter], axis=0))[0]
    return feature_subset
