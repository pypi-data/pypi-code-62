from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from ..figures import summary as summary_figures
from ..common import data


def add_projection_coloring(app):

    @app.callback(
        Output("projection_plot", "figure"),
        [Input("projection_color_choice", "value")]
    )
    def toggle_navbar_collapse(value):

        group_by = data.Cell_Grouping(value)

        return summary_figures.get_cell_tSNE_figure(group_by=group_by)
