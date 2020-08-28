"""
Library PDF reports
Author: Sergey Bobkov
"""

import datetime
from typing import Optional
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

mpl.rcParams['image.cmap'] = 'viridis'


class ReportWriter():
    """Produce PDF reports with tables and matplotlib figures"""
    def __init__(self, filename: str):
        self._create_file(filename)

    def _create_file(self, filename: str):
        self.pdf_pages = PdfPages(filename)
        pdf_dict = self.pdf_pages.infodict()
        pdf_dict['CreationDate'] = datetime.datetime.today()
        pdf_dict['ModDate'] = datetime.datetime.today()

    def save_table(self, data_frame: pd.DataFrame):
        """Add a page to PDF with table

        Keyword arguments:
        data_frame -- pandas dataframe to be saved
        """
        # Compute optimal columns width
        content_df = data_frame.copy()
        content_df.loc[len(content_df)] = data_frame.columns.values
        col_widhts = np.array([content_df.loc[:, c].apply(str).apply(len).max()\
                               for c in content_df.columns.values], dtype=np.float64)
        col_widhts *= 1/col_widhts.sum()

        fig, axes = plt.subplots(figsize=(10, len(content_df)/4 + 1))
        axes.axis('off')
        axes.axis('tight')

        axes.table(cellText=data_frame.values, colLabels=data_frame.columns, loc='center',
                   colWidths=col_widhts)

        fig.tight_layout()

        self.pdf_pages.savefig()

    def save_figure(self, figure: plt.Figure):
        """Add a page to PDF with matplotlib figure

        Keyword arguments:
        figure -- figure to be saved
        """

        self.pdf_pages.savefig(figure)
        plt.close(figure)


    def close(self):
        """Closes PDF document"""
        self.pdf_pages.close()


def plot_image(image: np.ndarray, axis: plt.Axes, logscale: bool = True,
               colorbar: bool = True, vmin: Optional[float] = None, vmax: Optional[float] = None,
               **kwargs):
    """Plot image to axis with optional logscale and colorbar

    Keyword arguments:
    image -- 2D array with data to show
    axis -- matplotlib axis to plot
    logscale -- use logscale
    colorbar -- add colorbar to image
    vmin -- minimal value of colormap
    vmax -- miximum value of colormap
    kwargs -- arguments for imshow
    """
    if vmin is None and logscale:
        vmin = max(1, np.amin(image))
    elif vmin is None:
        vmin = np.amin(image)

    if vmax is None:
        vmax = np.amax(image)

    if logscale:
        norm = colors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        norm = colors.Normalize(vmin=vmin, vmax=vmax)

    im_handle = axis.imshow(image, norm=norm, **kwargs)
    axis.set_xticks([])
    axis.set_yticks([])

    if colorbar:
        divider = make_axes_locatable(axis)
        cb_axis = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im_handle, cax=cb_axis)
