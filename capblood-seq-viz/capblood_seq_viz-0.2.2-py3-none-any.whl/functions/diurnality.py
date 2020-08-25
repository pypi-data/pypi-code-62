from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from .. import figures


def add_gene_click_listener(app):

    @app.callback(
        Output("diurnality_gene_dropdown", "value"),
        [
            Input("diurnality_plot", "clickData")
        ]
    )
    def update_gene_dropdown(click_data):

        if click_data is None:
            raise PreventUpdate

        gene_name = click_data["points"][0]["text"]

        return gene_name


def add_gene_selected_listener(app):

    @app.callback(
        Output("gene_AM_PM_box_plot", "figure"),
        [
            Input("diurnality_gene_dropdown", "value")
        ]
    )
    def update_gene_AM_PM_box_plots(gene):

        if gene is None:
            raise PreventUpdate

        return figures.diurnality.get_gene_AM_PM_box_plot(gene)

    @app.callback(
        Output("diurnal_gene_mean_trace", "figure"),
        [
            Input("diurnality_gene_dropdown", "value")
        ]
    )
    def update_gene_diurnal_traces(gene):

        if gene is None:
            raise PreventUpdate

        return figures.diurnality.get_gene_traces(gene)
