import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ..figures import summary as summary_figures
from ..common.data import Cell_Grouping


def summary_layout():

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="projection_plot",
                            figure=summary_figures.get_cell_tSNE_figure(),
                            style={
                                "width": "100%",
                                "height": "100%"
                            }
                        ),
                        width=9
                    ),
                    dbc.Col(
                        dbc.FormGroup(
                            [
                                dbc.Label(
                                    "Group By:"
                                ),
                                dbc.RadioItems(
                                    options=[
                                        {
                                            "label": grouping.to_name(),
                                            "value": grouping.value
                                        }
                                        for grouping in Cell_Grouping
                                        if grouping != Cell_Grouping.NONE
                                    ],
                                    value=Cell_Grouping.CELL_TYPE.value,
                                    id="projection_color_choice"
                                )
                            ]
                        )
                    )
                ],
                style={
                    "height": "50%"
                }
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="sunburst_plot",
                                figure=summary_figures.get_sunburst_figure(),
                                style={
                                    "width": "100%",
                                    "height": "100%"
                                }
                            )
                        ],
                        width=6
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="pathway_enrichment_plot",
                                figure=summary_figures.get_pathway_enrichment_figure(),
                                style={
                                    "width": "100%",
                                    "height": "100%"
                                }
                            )
                        ],
                        width=6
                    )
                ],
                style={
                    "height": "50%"
                }
            ),
        ],
        id="summary_container",
        style={
            "display": "none",
            "height": "100%"
        }
    )
