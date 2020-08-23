import collections.abc as cabc
import numpy as np
import pandas as pd
from cycler import Cycler
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.sparse import issparse
from matplotlib import pyplot as pl
from matplotlib import rcParams, cm, colors
from anndata import AnnData
from typing import Union, Optional, List, Sequence, Iterable

from .._utils import savefig_or_show
from ..._utils import _doc_params, sanitize_anndata, subsample
from ..._compat import Literal
from ... import logging as logg
from .._anndata import ranking
from .._utils import timeseries, timeseries_subplot, timeseries_as_heatmap
from ..._settings import settings
from .._docs import doc_scatter_embedding, doc_show_save_ax, doc_vminmax, doc_panels
from ...get import rank_features_groups_df
from .scatterplots import pca, embedding, _panel_grid
from matplotlib.colors import Colormap

# ------------------------------------------------------------------------------
# PCA
# ------------------------------------------------------------------------------


@_doc_params(scatter_bulk=doc_scatter_embedding, show_save_ax=doc_show_save_ax)
def pca_overview(adata: AnnData, **params):
    """\
    Plot PCA results.

    The parameters are the ones of the scatter plot. Call pca_ranking separately
    if you want to change the default settings.

    Parameters
    ----------
    adata
        Annotated data matrix.
    color
        Keys for observation/subject annotation either as list `["ann1", "ann2"]` or
        string `"ann1,ann2,..."`.
    use_raw
        Use `raw` attribute of `adata` if present.
    {scatter_bulk}
    show
         Show the plot, do not return axis.
    save
        If `True` or a `str`, save the figure.
        A string is appended to the default filename.
        Infer the filetype if ending on {{`'.pdf'`, `'.png'`, `'.svg'`}}.
    """
    show = params['show'] if 'show' in params else None
    if 'show' in params:
        del params['show']
    scatterplots.pca(adata, **params, show=False)
    pca_loadings(adata, show=False)
    pca_variance_ratio(adata, show=show)


# backwards compat
pca_scatter = pca


def pca_loadings(
    adata: AnnData,
    components: Union[str, Sequence[int], None] = None,
    include_lowest: bool = True,
    show: Optional[bool] = None,
    save: Union[str, bool, None] = None,
):
    """\
    Rank features according to contributions to PCs.

    Parameters
    ----------
    adata
        Annotated data matrix.
    components
        For example, ``'1,2,3'`` means ``[1, 2, 3]``, first, second, third
        principal component.
    include_lowest
        Show the features with both highest and lowest loadings.
    show
        Show the plot, do not return axis.
    save
        If `True` or a `str`, save the figure.
        A string is appended to the default filename.
        Infer the filetype if ending on {`'.pdf'`, `'.png'`, `'.svg'`}.
    """
    if components is None:
        components = [1, 2, 3]
    elif isinstance(components, str):
        components = [int(x) for x in components.split(',')]
    components = np.array(components) - 1
    if np.any(components < 0):
        logg.error("Component indices must be greater than zero.")
        return
    ranking(
        adata, 'varm', 'PCs', indices=components, include_lowest=include_lowest,
    )
    savefig_or_show('pca_loadings', show=show, save=save)


def pca_variance_ratio(
    adata: AnnData,
    n_pcs: int = 30,
    log: bool = False,
    show: Optional[bool] = None,
    save: Union[bool, str, None] = None,
):
    """\
    Plot the variance ratio.

    Parameters
    ----------
    n_pcs
         Number of PCs to show.
    log
         Plot on logarithmic scale..
    show
         Show the plot, do not return axis.
    save
        If `True` or a `str`, save the figure.
        A string is appended to the default filename.
        Infer the filetype if ending on {`'.pdf'`, `'.png'`, `'.svg'`}.
    """
    ranking(
        adata,
        'uns',
        'variance_ratio',
        n_points=n_pcs,
        dictionary='pca',
        labels='PC',
        log=log,
    )
    savefig_or_show('pca_variance_ratio', show=show, save=save)


# ------------------------------------------------------------------------------
# Subgroup identification and ordering – clustering, pseudotime, branching
# and tree inference tools
# ------------------------------------------------------------------------------


def dpt_timeseries(
    adata: AnnData,
    color_map: Union[str, Colormap] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    as_heatmap: bool = True,
):
    """\
    Heatmap of pseudotime series.

    Parameters
    ----------
    as_heatmap
        Plot the timeseries as heatmap.
    """
    if adata.n_vars > 100:
        logg.warning(
            'Plotting more than 100 features might take some while, '
            'consider selecting only highly variable features, for example.'
        )
    # only if number of features is not too high
    if as_heatmap:
        # plot time series as heatmap, as in Haghverdi et al. (2016), Fig. 1d
        timeseries_as_heatmap(
            adata.X[adata.obs['dpt_order_indices'].values],
            var_names=adata.var_names,
            highlights_x=adata.uns['dpt_changepoints'],
            color_map=color_map,
        )
    else:
        # plot time series as feature expression vs time
        timeseries(
            adata.X[adata.obs['dpt_order_indices'].values],
            var_names=adata.var_names,
            highlights_x=adata.uns['dpt_changepoints'],
            xlim=[0, 1.3 * adata.X.shape[0]],
        )
    pl.xlabel('dpt order')
    savefig_or_show('dpt_timeseries', save=save, show=show)


def dpt_groups_pseudotime(
    adata: AnnData,
    color_map: Union[str, Colormap, None] = None,
    palette: Union[Sequence[str], Cycler, None] = None,
    show: Optional[bool] = None,
    save: Union[bool, str, None] = None,
):
    """Plot groups and pseudotime."""
    _, (ax_grp, ax_ord) = pl.subplots(2, 1)
    timeseries_subplot(
        adata.obs['dpt_groups'].cat.codes,
        time=adata.obs['dpt_order'].values,
        color=np.asarray(adata.obs['dpt_groups']),
        highlights_x=adata.uns['dpt_changepoints'],
        ylabel='dpt groups',
        yticks=(
            np.arange(len(adata.obs['dpt_groups'].cat.categories), dtype=int)
            if len(adata.obs['dpt_groups'].cat.categories) < 5
            else None
        ),
        palette=palette,
        ax=ax_grp,
    )
    timeseries_subplot(
        adata.obs['dpt_pseudotime'].values,
        time=adata.obs['dpt_order'].values,
        color=adata.obs['dpt_pseudotime'].values,
        xlabel='dpt order',
        highlights_x=adata.uns['dpt_changepoints'],
        ylabel='pseudotime',
        yticks=[0, 1],
        color_map=color_map,
        ax=ax_ord,
    )
    savefig_or_show('dpt_groups_pseudotime', save=save, show=show)


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 20,
    feature_symbols: Optional[str] = None,
    key: Optional[str] = 'rank_features_groups',
    fontsize: int = 8,
    ncols: int = 4,
    sharey: bool = True,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    ax: Optional[Axes] = None,
    **kwds,
):
    """\
    Plot ranking of features.
    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    feature_symbols
        Key for field in `.var` that stores feature symbols if you do not want to
        use `.var_names`.
    n_features
        Number of features to show.
    fontsize
        Fontsize for feature names.
    ncols
        Number of panels shown per row.
    sharey
        Controls if the y-axis of each panels should be shared. But passing
        `sharey=False`, each panel has its own y-axis range.
    {show_save_ax}
    """
    if 'n_panels_per_row' in kwds:
        n_panels_per_row = kwds['n_panels_per_row']
    else:
        n_panels_per_row = ncols
    reference = str(adata.uns[key]['params']['reference'])
    group_names = adata.uns[key]['names'].dtype.names if groups is None else groups
    # one panel for each group
    # set up the figure
    n_panels_x = min(n_panels_per_row, len(group_names))
    n_panels_y = np.ceil(len(group_names) / n_panels_x).astype(int)

    from matplotlib import gridspec

    fig = pl.figure(
        figsize=(
            n_panels_x * rcParams['figure.figsize'][0],
            n_panels_y * rcParams['figure.figsize'][1],
        )
    )
    gs = gridspec.GridSpec(nrows=n_panels_y, ncols=n_panels_x, wspace=0.22, hspace=0.3)

    ax0 = None
    ymin = np.Inf
    ymax = -np.Inf
    for count, group_name in enumerate(group_names):
        feature_names = adata.uns[key]['names'][group_name][:n_features]
        scores = adata.uns[key]['scores'][group_name][:n_features]

        # Setting up axis, calculating y bounds
        if sharey:
            ymin = min(ymin, np.min(scores))
            ymax = max(ymax, np.max(scores))

            if ax0 is None:
                ax = fig.add_subplot(gs[count])
                ax0 = ax
            else:
                ax = fig.add_subplot(gs[count], sharey=ax0)
        else:
            ymin = np.min(scores)
            ymax = np.max(scores)
            ymax += 0.3 * (ymax - ymin)

            ax = fig.add_subplot(gs[count])
            ax.set_ylim(ymin, ymax)

        ax.set_xlim(-0.9, n_features - 0.1)

        # Mapping to feature_symbols
        if feature_symbols is not None:
            if adata.raw is not None and adata.uns[key]['params']['use_raw']:
                feature_names = adata.raw.var[feature_symbols][feature_names]
            else:
                feature_names = adata.var[feature_symbols][feature_names]

        # Making labels
        for ig, feature_name in enumerate(feature_names):
            ax.text(
                ig,
                scores[ig],
                feature_name,
                rotation='vertical',
                verticalalignment='bottom',
                horizontalalignment='center',
                fontsize=fontsize,
            )

        ax.set_title('{} vs. {}'.format(group_name, reference))
        if count >= n_panels_x * (n_panels_y - 1):
            ax.set_xlabel('ranking')

        # print the 'score' label only on the first panel per row.
        if count % n_panels_x == 0:
            ax.set_ylabel('score')

    if sharey is True:
        ymax += 0.3 * (ymax - ymin)
        ax.set_ylim(ymin, ymax)

    writekey = f"rank_features_groups_{adata.uns[key]['params']['groupby']}"
    savefig_or_show(writekey, show=show, save=save)


def _fig_show_save_or_axes(plot_obj, return_fig, show, save):
    """
     Decides what to return
     """
    if return_fig:
        return plot_obj
    else:
        plot_obj.make_figure()
        savefig_or_show(plot_obj.DEFAULT_SAVE_PREFIX, show=show, save=save)
        show = settings.autoshow if show is None else show
        if not show:
            return plot_obj.get_axes()


def _rank_features_groups_plot(
    adata: AnnData,
    plot_type: str = 'heatmap',
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    values_to_plot: Optional[str] = None,
    min_logfoldchange: Optional[float] = None,
    key: Optional[str] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    return_fig: Optional[bool] = False,
    **kwds,
):
    """\
    Common function to call the different rank_features_groups_* plots
    """
    if key is None:
        key = 'rank_features_groups'

    if groupby is None:
        groupby = str(adata.uns[key]['params']['groupby'])
    group_names = adata.uns[key]['names'].dtype.names if groups is None else groups

    var_names = {}  # dict in which each group is the key and the n_features are the values
    feature_names = []
    for group in group_names:
        if min_logfoldchange is not None:
            df = rank_features_groups_df(adata, group, key=key)
            # select features with given log_fold change
            features_list = df[df.logfoldchanges > min_logfoldchange].names.tolist()[
                :n_features
            ]
        else:
            # get all features that are 'non-nan'
            features_list = [
                feature for feature in adata.uns[key]['names'][group] if not pd.isnull(feature)
            ][:n_features]

        if len(features_list) == 0:
            logg.warning(f'No features found for group {group}')
            continue
        var_names[group] = features_list
        feature_names.extend(features_list)

    # by default add dendrogram to plots
    kwds.setdefault('dendrogram', True)

    if plot_type in ['dotplot', 'matrixplot']:
        # these two types of plots can also
        # show score, logfoldchange and pvalues, in general any value from rank
        # features groups
        title = None
        values_df = None
        if values_to_plot is not None:
            values_df = _get_values_to_plot(adata, values_to_plot, feature_names, key=key)
            title = values_to_plot

        if plot_type == 'dotplot':
            from .._dotplot import dotplot

            _pl = dotplot(
                adata,
                var_names,
                groupby,
                dot_color_df=values_df,
                return_fig=True,
                **kwds,
            )

            if title is not None:
                _pl.legend(colorbar_title=title.replace("_", " "))
        elif plot_type == 'matrixplot':
            from .._matrixplot import matrixplot

            _pl = matrixplot(
                adata, var_names, groupby, values_df=values_df, return_fig=True, **kwds
            )

            if title is not None:
                _pl.legend(title=title.replace("_", " "))

        return _fig_show_save_or_axes(_pl, return_fig, show, save)

    elif plot_type == 'stacked_violin':
        from .._stacked_violin import stacked_violin

        _pl = stacked_violin(adata, var_names, groupby, return_fig=True, **kwds)
        return _fig_show_save_or_axes(_pl, return_fig, show, save)

    elif plot_type == 'heatmap':
        from .._anndata import heatmap

        return heatmap(adata, var_names, groupby, show=show, save=save, **kwds)

    elif plot_type == 'tracksplot':
        from .._anndata import tracksplot

        return tracksplot(adata, var_names, groupby, show=show, save=save, **kwds)


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_heatmap(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    min_logfoldchange: Optional[float] = None,
    key: str = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    **kwds,
):
    """\
    Plot ranking of features using heatmap plot (see :func:`~quanp.pl.heatmap`)

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    n_features
        Number of features to show.
    groupby
        The key of the observation grouping to consider. By default,
        the groupby is chosen from the rank features groups parameter but
        other groupby options can be used.  It is expected that
        groupby is a categorical. If groupby is not a categorical observation,
        it would be subdivided into `num_categories` (see :func:`~quanp.pl.heatmap`).
    min_logfoldchange
        Value to filter features in groups if their logfoldchange is less than the
        min_logfoldchange
    key
        Key used to store the ranking results in `adata.uns`.
    **kwds
        Are passed to :func:`~quanp.pl.heatmap`.
    {show_save_ax}
    """
    return _rank_features_groups_plot(
        adata,
        plot_type='heatmap',
        groups=groups,
        n_features=n_features,
        groupby=groupby,
        key=key,
        min_logfoldchange=min_logfoldchange,
        show=show,
        save=save,
        **kwds,
    )


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_tracksplot(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    min_logfoldchange: Optional[float] = None,
    key: Optional[str] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    **kwds,
):
    """\
    Plot ranking of features using heatmap plot (see :func:`~quanp.pl.heatmap`)

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    n_features
        Number of features to show.
    groupby
        The key of the observation grouping to consider. By default,
        the groupby is chosen from the rank features groups parameter but
        other groupby options can be used.  It is expected that
        groupby is a categorical. If groupby is not a categorical observation,
        it would be subdivided into `num_categories` (see :func:`~quanp.pl.heatmap`).
    min_logfoldchange
        Value to filter features in groups if their logfoldchange is less than the
        min_logfoldchange
    key
        Key used to store the ranking results in `adata.uns`.
    **kwds
        Are passed to :func:`~quanp.pl.tracksplot`.
    {show_save_ax}
    """

    return _rank_features_groups_plot(
        adata,
        plot_type='tracksplot',
        groups=groups,
        n_features=n_features,
        groupby=groupby,
        key=key,
        min_logfoldchange=min_logfoldchange,
        show=show,
        save=save,
        **kwds,
    )


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_dotplot(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    values_to_plot: Optional[
        Literal[
            'score',
            'logfoldchanges',
            'pvals',
            'pvals_adj',
            'log10_pvals',
            'log10_pvals_adj',
        ]
    ] = None,
    min_logfoldchange: Optional[float] = None,
    key: Optional[str] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    return_fig: Optional[bool] = False,
    **kwds,
):
    """\
    Plot ranking of features using dotplot plot (see :func:`~quanp.pl.dotplot`)

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    n_features
        Number of features to show.
    groupby
        The key of the observation grouping to consider. By default,
        the groupby is chosen from the rank features groups parameter but
        other groupby options can be used.  It is expected that
        groupby is a categorical. If groupby is not a categorical observation,
        it would be subdivided into `num_categories` (see :func:`~quanp.pl.dotplot`).
    min_logfoldchange
        Value to filter features in groups if their logfoldchange is less than the
        min_logfoldchange
    key
        Key used to store the ranking results in `adata.uns`.
    {show_save_ax}
    return_fig
        Returns :class:`DotPlot` object. Useful for fine-tuning
        the plot. Takes precedence over `show=False`.
    **kwds
        Are passed to :func:`~quanp.pl.dotplot`.

    Returns
    -------
    If `return_fig` is `True`, returns a :class:`DotPlot` object,
    else if `show` is false, return axes dict

    Examples
    --------
    >>> import quanp as qp
    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> qp.tl.rank_features_groups(adata, 'bulk_labels', n_features=adata.raw.shape[1])

    Plot `logfoldchanges`, set manually min value to plot as -4 and max as 4
    and plot only features in each group that have a minimum log fold change of 3
    >>> qp.pl.rank_features_groups_dotplot(adata,
    ... n_features=4, values_to_plot="logfoldchanges",
    ... vmin=-5, vmax=5, min_logfoldchange=3)

    """

    return _rank_features_groups_plot(
        adata,
        plot_type='dotplot',
        groups=groups,
        n_features=n_features,
        groupby=groupby,
        values_to_plot=values_to_plot,
        key=key,
        min_logfoldchange=min_logfoldchange,
        show=show,
        save=save,
        return_fig=return_fig,
        **kwds,
    )


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_stacked_violin(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    min_logfoldchange: Optional[float] = None,
    key: Optional[str] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    return_fig: Optional[bool] = False,
    **kwds,
):
    """\
    Plot ranking of features using stacked_violin plot
    (see :func:`~quanp.pl.stacked_violin`)

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    n_features
        Number of features to show.
    groupby
        The key of the observation grouping to consider. By default,
        the groupby is chosen from the rank features groups parameter but
        other groupby options can be used.  It is expected that
        groupby is a categorical. If groupby is not a categorical observation,
        it would be subdivided into `num_categories` (see :func:`~quanp.pl.stacked_violin`).
    min_logfoldchange
        Value to filter features in groups if their logfoldchange is less than the
        min_logfoldchange
    key
        Key used to store the ranking results in `adata.uns`.
    {show_save_ax}
    return_fig
        Returns :class:`StackedViolin` object. Useful for fine-tuning
        the plot. Takes precedence over `show=False`.
    **kwds
        Are passed to :func:`~quanp.pl.stacked_violin`.

    Returns
    -------
    If `return_fig` is `True`, returns a :class:`StackedViolin` object,
    else if `show` is false, return axes dict

    Examples
    --------
    >>> import quanp as qp
    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> qp.tl.rank_features_groups(adata, 'bulk_labels', n_features=adata.raw.shape[1])

    >>> qp.pl.rank_features_groups_stacked_violin(adata, n_features=4,
    ... min_logfoldchange=4, figsize=(8,6))

    """

    return _rank_features_groups_plot(
        adata,
        plot_type='stacked_violin',
        groups=groups,
        n_features=n_features,
        groupby=groupby,
        key=key,
        min_logfoldchange=min_logfoldchange,
        show=show,
        save=save,
        return_fig=return_fig,
        **kwds,
    )


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_matrixplot(
    adata: AnnData,
    groups: Union[str, Sequence[str]] = None,
    n_features: int = 10,
    groupby: Optional[str] = None,
    min_logfoldchange: Optional[float] = None,
    key: Optional[str] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
    return_fig: Optional[bool] = False,
    **kwds,
):
    """\
    Plot ranking of features using matrixplot plot (see :func:`~quanp.pl.matrixplot`)

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        The groups for which to show the feature ranking.
    n_features
        Number of features to show.
    groupby
        The key of the observation grouping to consider. By default,
        the groupby is chosen from the rank features groups parameter but
        other groupby options can be used.  It is expected that
        groupby is a categorical. If groupby is not a categorical observation,
        it would be subdivided into `num_categories` (see :func:`~quanp.pl.matrixplot`).
    min_logfoldchange
        Value to filter features in groups if their logfoldchange is less than the
        min_logfoldchange
    key
        Key used to store the ranking results in `adata.uns`.
    {show_save_ax}
    return_fig
        Returns :class:`MatrixPlot` object. Useful for fine-tuning
        the plot. Takes precedence over `show=False`.
    **kwds
        Are passed to :func:`~quanp.pl.matrixplot`.

    Returns
    -------
    If `return_fig` is `True`, returns a :class:`MatrixPlot` object,
    else if `show` is false, return axes dict

    Examples
    --------
    >>> import quanp as qp
    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> qp.tl.rank_features_groups(adata, 'bulk_labels', n_features=adata.raw.shape[1])

    Plot `logfoldchanges`, set manually min value to plot as -4 and max as 4
    and plot only features in each group that have a minimum log fold change of 3
    >>> qp.pl.rank_features_groups_matrixplot(adata,
    ... n_features=4, values_to_plot="logfoldchanges",
    ... vmin=-5, vmax=5, min_logfoldchange=3)

    """

    return _rank_features_groups_plot(
        adata,
        plot_type='matrixplot',
        groups=groups,
        n_features=n_features,
        groupby=groupby,
        key=key,
        min_logfoldchange=min_logfoldchange,
        show=show,
        save=save,
        return_fig=return_fig,
        **kwds,
    )


@_doc_params(show_save_ax=doc_show_save_ax)
def rank_features_groups_violin(
    adata: AnnData,
    groups: Optional[Sequence[str]] = None,
    n_features: int = 20,
    feature_names: Optional[Iterable[str]] = None,
    feature_symbols: Optional[str] = None,
    use_raw: Optional[bool] = None,
    key: Optional[str] = None,
    split: bool = True,
    scale: str = 'width',
    strip: bool = True,
    jitter: Union[int, float, bool] = True,
    size: int = 1,
    ax: Optional[Axes] = None,
    show: Optional[bool] = None,
    save: Optional[bool] = None,
):
    """\
    Plot ranking of features for all tested comparisons.

    Parameters
    ----------
    adata
        Annotated data matrix.
    groups
        List of group names.
    n_features
        Number of features to show. Is ignored if `feature_names` is passed.
    feature_names
        List of features to plot. Is only useful if interested in a custom feature list,
        which is not the result of :func:`quanp.tl.rank_features_groups`.
    feature_symbols
        Key for field in `.var` that stores feature symbols if you do not want to
        use `.var_names` displayed in the plot.
    use_raw
        Use `raw` attribute of `adata` if present. Defaults to the value that
        was used in :func:`~quanp.tl.rank_features_groups`.
    split
        Whether to split the violins or not.
    scale
        See :func:`~seaborn.violinplot`.
    strip
        Show a strip plot on top of the violin plot.
    jitter
        If set to 0, no points are drawn. See :func:`~seaborn.stripplot`.
    size
        Size of the jitter points.
    {show_save_ax}
    """
    if key is None:
        key = 'rank_features_groups'
    groups_key = str(adata.uns[key]['params']['groupby'])
    if use_raw is None:
        use_raw = bool(adata.uns[key]['params']['use_raw'])
    reference = str(adata.uns[key]['params']['reference'])
    groups_names = adata.uns[key]['names'].dtype.names if groups is None else groups
    if isinstance(groups_names, str):
        groups_names = [groups_names]
    axs = []
    for group_name in groups_names:
        if feature_names is None:
            _feature_names = adata.uns[key]['names'][group_name][:n_features]
        else:
            _feature_names = feature_names
        df = pd.DataFrame()
        new_feature_names = []
        for g in _feature_names:
            if adata.raw is not None and use_raw:
                X_col = adata.raw[:, g].X
                if feature_symbols:
                    g = adata.raw.var[feature_symbols][g]
            else:
                X_col = adata[:, g].X
                if feature_symbols:
                    g = adata.var[feature_symbols][g]
            if issparse(X_col):
                X_col = X_col.toarray().flatten()
            new_feature_names.append(g)
            df[g] = X_col
        df['hue'] = adata.obs[groups_key].astype(str).values
        if reference == 'rest':
            df.loc[df['hue'] != group_name, 'hue'] = 'rest'
        else:
            df.loc[~df['hue'].isin([group_name, reference]), 'hue'] = np.nan
        df['hue'] = df['hue'].astype('category')
        df_tidy = pd.melt(df, id_vars='hue', value_vars=new_feature_names)
        x = 'variable'
        y = 'value'
        hue_order = [group_name, reference]
        import seaborn as sns

        _ax = sns.violinplot(
            x=x,
            y=y,
            data=df_tidy,
            inner=None,
            hue_order=hue_order,
            hue='hue',
            split=split,
            scale=scale,
            orient='vertical',
            ax=ax,
        )
        if strip:
            _ax = sns.stripplot(
                x=x,
                y=y,
                data=df_tidy,
                hue='hue',
                dodge=True,
                hue_order=hue_order,
                jitter=jitter,
                color='black',
                size=size,
                ax=_ax,
            )
        _ax.set_xlabel('features')
        _ax.set_title('{} vs. {}'.format(group_name, reference))
        _ax.legend_.remove()
        _ax.set_ylabel('expression')
        _ax.set_xticklabels(new_feature_names, rotation='vertical')
        writekey = (
            f"rank_features_groups_"
            f"{adata.uns[key]['params']['groupby']}_"
            f"{group_name}"
        )
        savefig_or_show(writekey, show=show, save=save)
        axs.append(_ax)
    if show == False:
        return axs


def sim(
    adata,
    tmax_realization: Optional[int] = None,
    as_heatmap: bool = False,
    shuffle: bool = False,
    show: Optional[bool] = None,
    save: Union[bool, str, None] = None,
):
    """\
    Plot results of simulation.

    Parameters
    ----------
    tmax_realization
        Number of observations in one realization of the time series. The data matrix
        adata.X consists in concatenated realizations.
    as_heatmap
        Plot the timeseries as heatmap.
    shuffle
        Shuffle the data.
    show
        Show the plot, do not return axis.
    save
        If `True` or a `str`, save the figure.
        A string is appended to the default filename.
        Infer the filetype if ending on {{`'.pdf'`, `'.png'`, `'.svg'`}}.
    """
    if tmax_realization is not None:
        tmax = tmax_realization
    elif 'tmax_write' in adata.uns:
        tmax = adata.uns['tmax_write']
    else:
        tmax = adata.n_obs
    n_realizations = adata.n_obs / tmax
    if not shuffle:
        if not as_heatmap:
            timeseries(
                adata.X,
                var_names=adata.var_names,
                xlim=[0, 1.25 * adata.n_obs],
                highlights_x=np.arange(tmax, n_realizations * tmax, tmax),
                xlabel='realizations',
            )
        else:
            # plot time series as heatmap, as in Haghverdi et al. (2016), Fig. 1d
            timeseries_as_heatmap(
                adata.X,
                var_names=adata.var_names,
                highlights_x=np.arange(tmax, n_realizations * tmax, tmax),
            )
        pl.xticks(
            np.arange(0, n_realizations * tmax, tmax),
            np.arange(n_realizations).astype(int) + 1,
        )
        savefig_or_show('sim', save=save, show=show)
    else:
        # shuffled data
        X = adata.X
        X, rows = subsample(X, seed=1)
        timeseries(
            X,
            var_names=adata.var_names,
            xlim=[0, 1.25 * adata.n_obs],
            highlights_x=np.arange(tmax, n_realizations * tmax, tmax),
            xlabel='index (arbitrary order)',
        )
        savefig_or_show('sim_shuffled', save=save, show=show)


@_doc_params(vminmax=doc_vminmax, panels=doc_panels, show_save_ax=doc_show_save_ax)
def embedding_density(
    adata: AnnData,
    # on purpose, there is no asterisk here (for backward compat)
    basis: str = 'umap',  # was positional before 1.4.5
    key: Optional[str] = None,  # was positional before 1.4.5
    groupby: Optional[str] = None,
    group: Optional[Union[str, List[str], None]] = 'all',
    color_map: Union[Colormap, str] = 'YlOrRd',
    bg_dotsize: Optional[int] = 80,
    fg_dotsize: Optional[int] = 180,
    vmax: Optional[int] = 1,
    vmin: Optional[int] = 0,
    ncols: Optional[int] = 4,
    hspace: Optional[float] = 0.25,
    wspace: Optional[None] = None,
    title: str = None,
    show: Optional[bool] = None,
    save: Union[bool, str, None] = None,
    ax: Optional[Axes] = None,
    return_fig: Optional[bool] = None,
    **kwargs,
) -> Union[Figure, Axes, None]:
    """\
    Plot the density of subjects in an embedding (per condition).

    Plots the gaussian kernel density estimates (over condition) from the
    `qp.tl.embedding_density()` output.


    Parameters
    ----------
    adata
        The annotated data matrix.
    basis
        The embedding over which the density was calculated. This embedded
        representation should be found in `adata.obsm['X_[basis]']``.
    key
        Name of the `.obs` covariate that contains the density estimates. Alternatively, pass `groupby`.
    groupby
        Name of the condition used in `tl.embedding_density`. Alternatively, pass `key`.
    group
        The category in the categorical observation annotation to be plotted.
        For example, 'G1' in the cell cycle 'phase' covariate. If all categories
        are to be plotted use group='all' (default), If multiple categories
        want to be plotted use a list (e.g.: ['G1', 'S']. If the overall density
        wants to be ploted set group to 'None'.
    color_map
        Matplolib color map to use for density plotting.
    bg_dotsize
        Dot size for background data points not in the `group`.
    fg_dotsize
        Dot size for foreground data points in the `group`.
    {vminmax}
    {panels}
    {show_save_ax}

    Examples
    --------
    >>> import quanp as qp
    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> qp.tl.umap(adata)
    >>> qp.tl.embedding_density(adata, basis='umap', groupby='phase')

    Plot all categories be default
    >>> qp.pl.embedding_density(adata, basis='umap', key='umap_density_phase')

    Plot selected categories
    >>> qp.pl.embedding_density(
    ...     adata,
    ...     basis='umap',
    ...     key='umap_density_phase',
    ...     group=['G1', 'S'],
    ... )
    """
    sanitize_anndata(adata)

    # Test user inputs
    basis = basis.lower()

    if basis == 'fa':
        basis = 'draw_graph_fa'

    if key is not None and groupby is not None:
        raise ValueError('either pass key or groupby but not both')

    if key is None:
        key = 'umap_density'
    if groupby is not None:
        key += f'_{groupby}'

    if f'X_{basis}' not in adata.obsm_keys():
        raise ValueError(
            f'Cannot find the embedded representation `adata.obsm[X_{basis!r}]`. '
            'Compute the embedding first.'
        )

    if key not in adata.obs or f'{key}_params' not in adata.uns:
        raise ValueError(
            'Please run `qp.tl.embedding_density()` first '
            'and specify the correct key.'
        )

    if 'components' in kwargs:
        logg.warning(
            'Components were specified, but will be ignored. Only the '
            'components used to calculate the density can be plotted.'
        )
        del kwargs['components']

    components = adata.uns[f'{key}_params']['components']
    groupby = adata.uns[f'{key}_params']['covariate']

    # turn group into a list if needed
    if group == 'all':
        if groupby is None:
            group = None
        else:
            group = list(adata.obs[groupby].cat.categories)
    elif isinstance(group, str):
        group = [group]

    if group is None and groupby is not None:
        raise ValueError(
            'Densities were calculated over an `.obs` covariate. '
            'Please specify a group from this covariate to plot.'
        )

    if group is not None and groupby is None:
        logg.warning(
            "value of 'group' is ignored because densities "
            "were not calculated for an `.obs` covariate."
        )
        group = None

    if np.min(adata.obs[key]) < 0 or np.max(adata.obs[key]) > 1:
        raise ValueError('Densities should be scaled between 0 and 1.')

    if wspace is None:
        #  try to set a wspace that is not too large or too small given the
        #  current figure size
        wspace = 0.75 / rcParams['figure.figsize'][0] + 0.02

    # Make the color map
    if isinstance(color_map, str):
        color_map = cm.get_cmap(color_map)

    norm = colors.Normalize(vmin=vmin, vmax=vmax)
    color_map.set_over('black')
    color_map.set_under('lightgray')
    # a name to store the density values is needed. To avoid
    # overwriting a user name a new random name is created
    while True:
        col_id = np.random.randint(1000, 10000)
        density_col_name = f'_tmp_embedding_density_column_{col_id}_'
        if density_col_name not in adata.obs.columns:
            break

    # if group is set, then plot it using multiple panels
    # (even if only one group is set)
    if (
        group is not None
        and not isinstance(group, str)
        and isinstance(group, cabc.Sequence)
    ):
        if ax is not None:
            raise ValueError("Can only specify `ax` if no `group` sequence is given.")
        fig, gs = _panel_grid(hspace, wspace, ncols, len(group))

        axs = []
        for count, group_name in enumerate(group):
            if group_name not in adata.obs[groupby].cat.categories:
                raise ValueError(
                    'Please specify a group from the `.obs` category '
                    'over which the density was calculated. '
                    f'Invalid group name: {group_name}'
                )

            ax = pl.subplot(gs[count])
            # Define plotting data
            dot_sizes = np.ones(adata.n_obs) * bg_dotsize
            group_mask = adata.obs[groupby] == group_name
            dens_values = -np.ones(adata.n_obs)
            dens_values[group_mask] = adata.obs[key][group_mask]
            adata.obs[density_col_name] = dens_values
            dot_sizes[group_mask] = np.ones(sum(group_mask)) * fg_dotsize

            if title is None:
                _title = group_name
            else:
                _title = title

            ax = embedding(
                adata,
                basis,
                components=components,
                color=density_col_name,
                color_map=color_map,
                norm=norm,
                size=dot_sizes,
                vmax=vmax,
                vmin=vmin,
                save=False,
                title=_title,
                ax=ax,
                show=False,
                **kwargs,
            )
            axs.append(ax)

        ax = axs
    else:
        dens_values = adata.obs[key]
        dot_sizes = np.ones(adata.n_obs) * fg_dotsize

        adata.obs[density_col_name] = dens_values

        # Ensure title is blank as default
        if title is None:
            title = group if group is not None else ""

        # Plot the graph
        fig_or_ax = embedding(
            adata,
            basis,
            components=components,
            color=density_col_name,
            color_map=color_map,
            norm=norm,
            size=dot_sizes,
            vmax=vmax,
            vmin=vmin,
            save=False,
            show=False,
            title=title,
            ax=ax,
            return_fig=return_fig,
            **kwargs,
        )
        if return_fig:
            fig = fig_or_ax
        else:
            ax = fig_or_ax

    # remove temporary column name
    adata.obs = adata.obs.drop(columns=[density_col_name])

    if return_fig:
        return fig
    savefig_or_show(f"{key}_", show=show, save=save)
    if show is False:
        return ax


def _get_values_to_plot(
    adata,
    values_to_plot: Literal[
        'scores',
        'logfoldchanges',
        'pvals',
        'pvals_adj',
        'log10_pvals',
        'log10_pvals_adj',
    ],
    feature_names: Sequence[str],
    groups: Optional[Sequence[str]] = None,
    key: Optional[str] = 'rank_features_groups',
):
    """
    If rank_features_groups has been called, this function
    prepares a dataframe containing scores, pvalues, logfoldchange etc to be plotted
    as dotplot or matrixplot.

    The dataframe index are the given groups and the columns are the feature_names

    uset for rank_features_groups_dotplot

    Parameters
    ----------
    adata
    values_to_plot
        name of the value to plot
    feature_names
        feature names
    groups
        groupby categories
    key
        adata.uns key where the rank_features_groups is stored. By default 'rank_features_groups'
    Returns
    -------
    pandas DataFrame index=groups, columns=feature_names

    """
    values_df = None
    check_done = False
    if groups is None:
        groups = adata.uns[key]['names'].dtype.names
    if values_to_plot is not None:

        df_list = []
        for group in groups:
            df = rank_features_groups_df(adata, group, key=key)
            # check that all features are present as by default rank_features_groups
            # only report the top 100 features per category
            if not check_done:
                if df.shape[0] < adata.shape[1]:
                    message = (
                        "Please run `qp.tl.rank_features_groups` with "
                        "'n_features=adata.shape[1]' to save all feature "
                        f"scores. Currently, only {df.shape[0]} "
                        "are found"
                    )
                    logg.error(message)
                    raise ValueError(message)
            df['group'] = group
            df_list.append(df)

        values_df = pd.concat(df_list)
        if values_to_plot.startswith('log10'):
            column = values_to_plot.replace('log10_', '')
        else:
            column = values_to_plot
        values_df = pd.pivot(
            values_df, index='names', columns='group', values=column
        ).fillna(1)

        if values_to_plot in ['log10_pvals', 'log10_pvals_adj']:
            values_df = -1 * np.log10(values_df)

        values_df = values_df.loc[feature_names].T

    return values_df
