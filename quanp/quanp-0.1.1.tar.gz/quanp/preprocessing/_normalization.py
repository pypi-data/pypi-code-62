from typing import Optional, Union, Iterable, Dict

import numpy as np
from anndata import AnnData
from scipy.sparse import issparse
from sklearn.utils import sparsefuncs

from .. import logging as logg
from .._compat import Literal
from .._utils import view_to_actual


def _normalize_data(X, counts, after=None, copy=False):
    X = X.copy() if copy else X
    if issubclass(X.dtype.type, (int, np.integer)):
        X = X.astype(np.float32)  # TODO: Check if float64 should be used
    counts = np.asarray(counts)  # dask doesn't do medians
    after = np.median(counts[counts>0], axis=0) if after is None else after
    counts += (counts == 0)
    counts = counts / after
    if issparse(X):
        sparsefuncs.inplace_row_scale(X, 1/counts)
    else:
        np.divide(X, counts[:, None], out=X)
    return X


def normalize_total(
    adata: AnnData,
    target_sum: Optional[float] = None,
    exclude_highly_expressed: bool = False,
    max_fraction: float = 0.05,
    key_added: Optional[str] = None,
    layers: Union[Literal['all'], Iterable[str]] = None,
    layer_norm: Optional[str] = None,
    inplace: bool = True,
) -> Optional[Dict[str, np.ndarray]]:
    """\
    Normalize counts per subject.
    If choosing `target_sum=1e6`, this is CPM normalization.
    If `exclude_highly_expressed=True`, very highly expressed features are excluded
    from the computation of the normalization factor (size factor) for each
    subject. This is meaningful as these can strongly influence the resulting
    normalized values for all other features [Weinreb17]_.
    Similar functions are used, for example, by Seurat [Satija15]_, Cell Ranger
    [Zheng17]_ or SPRING [Weinreb17]_.
    Params
    ------
    adata
        The annotated data matrix of shape `n_obs` × `n_vars`.
        Rows correspond to subjects and columns to features.
    target_sum
        If `None`, after normalization, each observation (subject) has a total
        count equal to the median of total counts for observations (subjects)
        before normalization.
    exclude_highly_expressed
        Exclude (very) highly expressed features for the computation of the
        normalization factor (size factor) for each subject. A feature is considered
        highly expressed, if it has more than `max_fraction` of the total counts
        in at least one subject. The not-excluded features will sum up to
        `target_sum`.
    max_fraction
        If `exclude_highly_expressed=True`, consider subjects as highly expressed
        that have more counts than `max_fraction` of the original total counts
        in at least one subject.
    key_added
        Name of the field in `adata.obs` where the normalization factor is
        stored.
    layers
        List of layers to normalize. Set to `'all'` to normalize all layers.
    layer_norm
        Specifies how to normalize layers:
        * If `None`, after normalization, for each layer in *layers* each subject
          has a total count equal to the median of the *counts_per_subject* before
          normalization of the layer.
        * If `'after'`, for each layer in *layers* each subject has
          a total count equal to `target_sum`.
        * If `'X'`, for each layer in *layers* each subject has a total count
          equal to the median of total counts for observations (subjects) of
          `adata.X` before normalization.
    inplace
        Whether to update `adata` or return dictionary with normalized copies of
        `adata.X` and `adata.layers`.
    Returns
    -------
    Returns dictionary with normalized copies of `adata.X` and `adata.layers`
    or updates `adata` with normalized version of the original
    `adata.X` and `adata.layers`, depending on `inplace`.
    Example
    --------
    >>> from anndata import AnnData
    >>> import scanpy as sc
    >>> sc.settings.verbosity = 2
    >>> np.set_printoptions(precision=2)
    >>> adata = AnnData(np.array([
    ...    [3, 3, 3, 6, 6],
    ...    [1, 1, 1, 2, 2],
    ...    [1, 22, 1, 2, 2],
    ... ]))
    >>> adata.X
    array([[ 3.,  3.,  3.,  6.,  6.],
           [ 1.,  1.,  1.,  2.,  2.],
           [ 1., 22.,  1.,  2.,  2.]], dtype=float32)
    >>> X_norm = sc.pp.normalize_total(adata, target_sum=1, inplace=False)['X']
    >>> X_norm
    array([[0.14, 0.14, 0.14, 0.29, 0.29],
           [0.14, 0.14, 0.14, 0.29, 0.29],
           [0.04, 0.79, 0.04, 0.07, 0.07]], dtype=float32)
    >>> X_norm = sc.pp.normalize_total(
    ...     adata, target_sum=1, exclude_highly_expressed=True,
    ...     max_fraction=0.2, inplace=False
    ... )['X']
    The following highly-expressed features are not considered during normalization factor computation:
    ['1', '3', '4']
    >>> X_norm
    array([[ 0.5,  0.5,  0.5,  1. ,  1. ],
           [ 0.5,  0.5,  0.5,  1. ,  1. ],
           [ 0.5, 11. ,  0.5,  1. ,  1. ]], dtype=float32)
    """
    if max_fraction < 0 or max_fraction > 1:
        raise ValueError('Choose max_fraction between 0 and 1.')

    if layers == 'all':
        layers = adata.layers.keys()
    elif isinstance(layers, str):
        raise ValueError(
            f"`layers` needs to be a list of strings or 'all', not {layers!r}"
        )

    view_to_actual(adata)

    feature_subset = None
    msg = 'normalizing counts per subject'
    if exclude_highly_expressed:
        counts_per_subject = adata.X.sum(1)  # original counts per subject
        counts_per_subject = np.ravel(counts_per_subject)

        # at least one subject as more than max_fraction of counts per subject
        feature_subset = (adata.X > counts_per_subject[:, None]*max_fraction).sum(0)
        feature_subset = (np.ravel(feature_subset) == 0)

        msg += (
            ' The following highly-expressed features are not considered during '
            f'normalization factor computation:\n{adata.var_names[~feature_subset].tolist()}'
        )
    start = logg.info(msg)

    # counts per subject for subset, if max_fraction!=1
    X = adata.X if feature_subset is None else adata[:, feature_subset].X
    counts_per_subject = X.sum(1)
    # get rid of adata view
    counts_per_subject = np.ravel(counts_per_subject).copy()

    subject_subset = counts_per_subject > 0
    if not np.all(subject_subset):
        logg.warning('Some subjects have total count of features equal to zero')

    if layer_norm == 'after':
        after = target_sum
    elif layer_norm == 'X':
        after = np.median(counts_per_subject[subject_subset])
    elif layer_norm is None:
        after = None
    else:
        raise ValueError('layer_norm should be "after", "X" or None')
    del subject_subset

    if inplace:
        if key_added is not None:
            adata.obs[key_added] = counts_per_subject
        adata.X = _normalize_data(adata.X, counts_per_subject, target_sum)
    else:
        # not recarray because need to support sparse
        dat = dict(
            X=_normalize_data(adata.X, counts_per_subject, target_sum, copy=True),
            norm_factor=counts_per_subject,
        )

    for layer_name in (layers or ()):
        layer = adata.layers[layer_name]
        counts = np.ravel(layer.sum(1))
        if inplace:
            adata.layers[layer_name] = _normalize_data(layer, counts, after)
        else:
            dat[layer_name] = _normalize_data(layer, counts, after, copy=True)

    logg.info(
        '    finished ({time_passed})',
        time=start,
    )
    if key_added is not None:
        logg.debug(f'and added {key_added!r}, counts per subject before normalization (adata.obs)')

    return dat if not inplace else None
