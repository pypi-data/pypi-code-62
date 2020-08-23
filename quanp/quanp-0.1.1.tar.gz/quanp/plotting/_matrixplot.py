from typing import Optional, Union, Mapping  # Special
from typing import Sequence  # ABCs
from typing import Tuple  # Classes

import numpy as np
import pandas as pd
from anndata import AnnData
from matplotlib import pyplot as pl
from matplotlib import rcParams

from .. import logging as logg
from .._utils import _doc_params
from .._compat import Literal
from ._utils import fix_kwds
from ._utils import ColorLike, _AxesSubplot
from ._utils import savefig_or_show
from .._settings import settings
from ._docs import doc_common_plot_args, doc_show_save_ax
from ._baseplot_class import BasePlot, doc_common_groupby_plot_args, _VarNames


@_doc_params(common_plot_args=doc_common_plot_args)
class MatrixPlot(BasePlot):
    """\
    Allows the visualization of values using a color map.

    Parameters
    ----------
    {common_plot_args}
    title
        Title for the figure.
    expression_cutoff
        Expression cutoff that is used for binarizing the feature expression and
        determining the fraction of subjects expressing given features. A feature is
        expressed only if the expression value is greater than this threshold.
    mean_only_expressed
        If True, feature expression is averaged only over the subjects
        expressing the given features.
    standard_scale
        Whether or not to standardize that dimension between 0 and 1,
        meaning for each variable or group,
        subtract the minimum and divide each by its maximum.
    values_df
        Optionally, a dataframe with the values to plot can be given. The
        index should be the grouby categories and the columns the features names.

    kwds
        Are passed to :func:`matplotlib.pyplot.scatter`.

    See also
    --------
    :func:`~quanp.pl.matrixplot`: Simpler way to call MatrixPlot but with less options.
    :func:`~quanp.pl.rank_features_groups_matrixplot`: to plot marker features identified
        using the :func:`~quanp.tl.rank_features_groups` function.

    Examples
    --------

    Simple visualization of the average expression of a few features grouped by
    the category 'bulk_labels'.

    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> markers = ['featureA', 'featureB', 'featureC', 'featureD', 'featureE', 'featureF']
    >>> qp.pl.MatrixPlot(adata, markers, groupby='bulk_labels').show()

    Same visualization but passing var_names as dict, which adds a grouping of
    the features on top of the image:

    >>> markers = {{'A-subject': 'featureA', 'B-subject': 'featureB', 'C-subject': 'featureC'}}
    >>> qp.pl.MatrixPlot(adata, markers, groupby='bulk_labels').show()
    """

    DEFAULT_SAVE_PREFIX = 'matrixplot_'
    DEFAULT_COLOR_LEGEND_TITLE = 'Mean expression\nin group'

    # default style parameters
    DEFAULT_COLORMAP = rcParams['image.cmap']
    DEFAULT_EDGE_COLOR = 'gray'
    DEFAULT_EDGE_LW = 0.1

    def __init__(
        self,
        adata: AnnData,
        var_names: Union[_VarNames, Mapping[str, _VarNames]],
        groupby: Union[str, Sequence[str]],
        use_raw: Optional[bool] = None,
        log: bool = False,
        num_categories: int = 7,
        categories_order: Optional[Sequence[str]] = None,
        title: Optional[str] = None,
        figsize: Optional[Tuple[float, float]] = None,
        feature_symbols: Optional[str] = None,
        var_group_positions: Optional[Sequence[Tuple[int, int]]] = None,
        var_group_labels: Optional[Sequence[str]] = None,
        var_group_rotation: Optional[float] = None,
        layer: Optional[str] = None,
        standard_scale: Literal['var', 'group'] = None,
        ax: Optional[_AxesSubplot] = None,
        values_df: Optional[pd.DataFrame] = None,
        **kwds,
    ):
        BasePlot.__init__(
            self,
            adata,
            var_names,
            groupby,
            use_raw=use_raw,
            log=log,
            num_categories=num_categories,
            categories_order=categories_order,
            title=title,
            figsize=figsize,
            feature_symbols=feature_symbols,
            var_group_positions=var_group_positions,
            var_group_labels=var_group_labels,
            var_group_rotation=var_group_rotation,
            layer=layer,
            ax=ax,
            **kwds,
        )

        if values_df is None:
            # compute mean value
            values_df = self.obs_tidy.groupby(level=0).mean()

            if standard_scale == 'group':
                values_df = values_df.sub(values_df.min(1), axis=0)
                values_df = values_df.div(values_df.max(1), axis=0).fillna(0)
            elif standard_scale == 'var':
                values_df -= values_df.min(0)
                values_df = (values_df / values_df.max(0)).fillna(0)
            elif standard_scale is None:
                pass
            else:
                logg.warning('Unknown type for standard_scale, ignored')

        self.values_df = values_df

        self.cmap = self.DEFAULT_COLORMAP
        self.edge_color = self.DEFAULT_EDGE_COLOR
        self.edge_lw = self.DEFAULT_EDGE_LW

    def style(
        self,
        cmap: str = DEFAULT_COLORMAP,
        edge_color: Optional[ColorLike] = DEFAULT_EDGE_COLOR,
        edge_lw: Optional[float] = DEFAULT_EDGE_LW,
    ):
        """\
        Modifies plot visual parameters.

        Parameters
        ----------
        cmap
            String denoting matplotlib color map.
        edge_color
            Edge color between the squares of matrix plot. Default is gray
        edge_lw
            Edge line width.

        Returns
        -------
        :class:`~quanp.pl.MatrixPlot`

        Examples
        -------

        >>> adata = qp.datasets.pbmc68k_reduced()
        >>> markers = ['featureA', 'featureB', 'featureC', 'featureD', 'featureE', 'featureF']

        Change color map and turn off edges:

        >>> qp.pl.MatrixPlot(adata, markers, groupby='bulk_labels')\
        ...               .style(cmap='Blues', edge_color='none').show()

        """

        # change only the values that had changed
        if cmap != self.cmap:
            self.cmap = cmap
        if edge_color != self.edge_color:
            self.edge_color = edge_color
        if edge_lw != self.edge_lw:
            self.edge_lw = edge_lw

        return self

    def _mainplot(self, ax):
        # work on a copy of the dataframes. This is to avoid changes
        # on the original data frames after repetitive calls to the
        # MatrixPlot object, for example once with swap_axes and other without

        _color_df = self.values_df.copy()
        if self.var_names_idx_order is not None:
            _color_df = _color_df.iloc[:, self.var_names_idx_order]

        if self.categories_order is not None:
            _color_df = _color_df.loc[self.categories_order, :]

        if self.are_axes_swapped:
            _color_df = _color_df.T
        cmap = pl.get_cmap(self.kwds.get('cmap', self.cmap))
        if 'cmap' in self.kwds:
            del self.kwds['cmap']

        import matplotlib.colors

        normalize = matplotlib.colors.Normalize(
            vmin=self.kwds.get('vmin'), vmax=self.kwds.get('vmax')
        )

        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(1.5)

        kwds = fix_kwds(
            self.kwds,
            cmap=cmap,
            edgecolor=self.edge_color,
            linewidth=self.edge_lw,
            norm=normalize,
        )
        __ = ax.pcolor(_color_df, **kwds)

        y_labels = _color_df.index
        x_labels = _color_df.columns

        y_ticks = np.arange(len(y_labels)) + 0.5
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)

        x_ticks = np.arange(len(x_labels)) + 0.5
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, rotation=90, ha='center', minor=False)

        ax.tick_params(axis='both', labelsize='small')
        ax.grid(False)

        # to be consistent with the heatmap plot, is better to
        # invert the order of the y-axis, such that the first group is on
        # top
        ax.set_ylim(len(y_labels), 0)
        ax.set_xlim(0, len(x_labels))

        return normalize


@_doc_params(
    show_save_ax=doc_show_save_ax,
    common_plot_args=doc_common_plot_args,
    groupby_plots_args=doc_common_groupby_plot_args,
)
def matrixplot(
    adata: AnnData,
    var_names: Union[_VarNames, Mapping[str, _VarNames]],
    groupby: Union[str, Sequence[str]],
    use_raw: Optional[bool] = None,
    log: bool = False,
    num_categories: int = 7,
    figsize: Optional[Tuple[float, float]] = None,
    dendrogram: Union[bool, str] = False,
    title: Optional[str] = None,
    cmap: Optional[str] = MatrixPlot.DEFAULT_COLORMAP,
    colorbar_title: Optional[str] = MatrixPlot.DEFAULT_COLOR_LEGEND_TITLE,
    feature_symbols: Optional[str] = None,
    var_group_positions: Optional[Sequence[Tuple[int, int]]] = None,
    var_group_labels: Optional[Sequence[str]] = None,
    var_group_rotation: Optional[float] = None,
    layer: Optional[str] = None,
    standard_scale: Literal['var', 'group'] = None,
    values_df: Optional[pd.DataFrame] = None,
    swap_axes: bool = False,
    show: Optional[bool] = None,
    save: Union[str, bool, None] = None,
    ax: Optional[_AxesSubplot] = None,
    return_fig: Optional[bool] = False,
    **kwds,
) -> Union[MatrixPlot, dict, None]:
    """\
    Creates a heatmap of the mean expression values per group of each var_names.

    This function provides a convenient interface to the :class:`~quanp.pl.MatrixPlot`
    class. If you need more flexibility, you should use :class:`~quanp.pl.MatrixPlot`
    directly.

    Parameters
    ----------
    {common_plot_args}
    {groupby_plots_args}
    {show_save_ax}
    kwds
        Are passed to :func:`matplotlib.pyplot.pcolor`.

    Returns
    -------
    If `return_fig` is `True`, returns a :class:`~quanp.pl.MatrixPlot` object,
    else if `show` is false, return axes dict

    See also
    --------
    :class:`~quanp.pl.MatrixPlot`: The MatrixPlot class can be used to to control
        several visual parameters not available in this function.
    :func:`~quanp.pl.rank_features_groups_matrixplot`: to plot marker features
        identified using the :func:`~quanp.tl.rank_features_groups` function.

    Examples
    --------

    >>> import quanp as qp
    >>> adata = qp.datasets.pbmc68k_reduced()
    >>> markers = ['featureA', 'featureB', 'featureC', 'featureD', 'featureE', 'featureF']
    >>> qp.pl.matrixplot(adata, markers, groupby='bulk_labels', dendrogram=True)

    Using var_names as dict:

    >>> markers = {{'A-subject': 'featureA', 'B-subject': 'featureB', 'C-subject': 'featureC'}}
    >>> qp.pl.matrixplot(adata, markers, groupby='bulk_labels', dendrogram=True)

    Get Matrix object for fine tuning:

    >>> mp = qp.pl.matrix(adata, markers, 'bulk_labels', return_fig=True)
    >>> mp.add_totals().style(edge_color='black').show()

    The axes used can be obtained using the get_axes() method

    >>> axes_dict = mp.get_axes()
    """

    mp = MatrixPlot(
        adata,
        var_names,
        groupby=groupby,
        use_raw=use_raw,
        log=log,
        num_categories=num_categories,
        standard_scale=standard_scale,
        title=title,
        figsize=figsize,
        feature_symbols=feature_symbols,
        var_group_positions=var_group_positions,
        var_group_labels=var_group_labels,
        var_group_rotation=var_group_rotation,
        layer=layer,
        values_df=values_df,
        ax=ax,
        **kwds,
    )

    if dendrogram:
        mp.add_dendrogram(dendrogram_key=dendrogram)
    if swap_axes:
        mp.swap_axes()

    mp = mp.style(cmap=cmap).legend(title=colorbar_title)
    if return_fig:
        return mp
    else:
        mp.make_figure()
        savefig_or_show(MatrixPlot.DEFAULT_SAVE_PREFIX, show=show, save=save)
        show = settings.autoshow if show is None else show
        if not show:
            return mp.get_axes()
