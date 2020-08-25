import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ..figures import diurnality
from ..data import diurnality as data


def diurnality_layout():

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="diurnality_plot",
                            figure=diurnality.get_diurnality_figure(),
                            style={
                                "width": "100%",
                                "height": "100%"
                            }
                        ),
                        width=9
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Label("Gene:")
                            ),
                            dcc.Dropdown(
                                id="diurnality_gene_dropdown",
                                options=data.get_gene_options(),
                                value=[],
                                multi=False
                            )
                        ],
                        width=3
                    )
                ],
                style={
                    "height": "50%"
                }
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="gene_AM_PM_box_plot",
                            figure={},
                            style={
                                "width": "100%",
                                "height": "100%"
                            },
                            config={
                                "displayModeBar": False
                            }
                        ),
                        width=9
                    ),
                ],
                style={
                    "height": "50%"
                }
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="diurnal_gene_mean_trace",
                            figure={},
                            style={
                                "width": "100%",
                                "height": "100%"
                            },
                            config={
                                "displayModeBar": False
                            }
                        ),
                        width=12
                    ),
                ],
                style={
                    "height": "35%"
                }
            )
        ],
        id="diurnality_container",
        style={
            "display": "none",
            "height": "100%"
        }
    )
