import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ..figures import individuality
from ..data import individuality as data


def individuality_layout():

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="individuality_plot",
                            figure=individuality.get_individuality_figure(),
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
                                id="individuality_gene_dropdown",
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
                            id="individual_gene_mean_trace",
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
        id="individuality_container",
        style={
            "display": "none",
            "height": "100%"
        }
    )
