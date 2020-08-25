import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from .. import config
from ..common import resources
from .about import about_layout
from .summary import summary_layout
from .diurnality import diurnality_layout
from .individuality import individuality_layout


def get_layout():
    return html.Div(
        children=[
            dcc.Store(id="tab_state"),
            dbc.Navbar(dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Img(
                                src=resources.get_asset_path("blood_logo.png"),
                                height="30px")
                            ),
                            dbc.Col(dbc.NavbarBrand(config.get("app_name")))
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.NavLink(
                                        "About",
                                        href="#",
                                        id="about_btn"
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.NavLink(
                                        "Summary",
                                        href="#",
                                        id="summary_btn"
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.NavLink(
                                        "Diurnality",
                                        href="#",
                                        id="diurnality_btn"
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.NavLink(
                                        "Individuality",
                                        href="#",
                                        id="individuality_btn"
                                    )
                                )
                            ],
                            navbar=True
                        ),
                        id="navbar-collapse",
                        navbar=True,
                    )
                ]),
                color="primary",
                dark=True
            ),
            about_layout(),
            summary_layout(),
            diurnality_layout(),
            individuality_layout()
        ],
        style={
            "height": "100vh"
        }
    )
