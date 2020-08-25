from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


def add_navbar_collapse(app):

    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(num_clicks, is_open):
        if num_clicks:
            return not is_open
        return is_open


def add_tab_switching(app):

    @app.callback(
        Output("about_container", "hidden"),
        [
            Input("tab_state", "data")
        ]
    )
    def about_button_hide(
            tab_state
    ):

        if tab_state is None:
            raise PreventUpdate

        return tab_state["about_tab_hidden"]

    @app.callback(
        Output("summary_container", "style"),
        [
            Input("tab_state", "data")
        ],
        [
            State("summary_container", "style")
        ]
    )
    def summary_button_style(tab_state, current_style):

        if tab_state is None:
            raise PreventUpdate

        if tab_state["summary_tab_hidden"]:
            current_style["display"] = "none"
        else:
            current_style["display"] = "block"

        return current_style

    @app.callback(
        Output("diurnality_container", "style"),
        [
            Input("tab_state", "data")
        ],
        [
            State("diurnality_container", "style")
        ]
    )
    def diurnality_button_style(tab_state, current_style):

        if tab_state is None:
            raise PreventUpdate

        if tab_state["diurnality_tab_hidden"]:
            current_style["display"] = "none"
        else:
            current_style["display"] = "block"

        return current_style

    @app.callback(
        Output("individuality_container", "style"),
        [
            Input("tab_state", "data")
        ],
        [
            State("individuality_container", "style")
        ]
    )
    def individuality_button_style(tab_state, current_style):

        if tab_state is None:
            raise PreventUpdate

        if tab_state["individuality_tab_hidden"]:
            current_style["display"] = "none"
        else:
            current_style["display"] = "block"

        return current_style

    @app.callback(
        Output("tab_state", "data"),
        [
            Input("about_btn", "n_clicks"),
            Input("summary_btn", "n_clicks"),
            Input("diurnality_btn", "n_clicks"),
            Input("individuality_btn", "n_clicks")
        ],
        [
            State("tab_state", "data")
        ]
    )
    def on_summary_button_clicked(
            num_about_clicks,
            num_summary_clicks,
            num_diurnality_clicks,
            num_individuality_clicks,
            tab_state):

        if num_about_clicks is None and \
                num_summary_clicks is None and \
                num_diurnality_clicks is None and \
                num_individuality_clicks is None:
            raise PreventUpdate

        # Give a default data dict with 0 clicks if there's no data.
        tab_state = tab_state or {
            "about_btn_clicks": None,
            "summary_btn_clicks": None,
            "diurnality_btn_clicks": None,
            "individuality_btn_clicks": None,
            "about_tab_hidden": True,
            "summary_tab_hidden": True,
            "diurnality_tab_hidden": True,
            "individuality_tab_hidden": True
        }

        tab_state["about_tab_hidden"] = True
        tab_state["summary_tab_hidden"] = True
        tab_state["diurnality_tab_hidden"] = True
        tab_state["individuality_tab_hidden"] = True

        if tab_state["about_btn_clicks"] != num_about_clicks:
            tab_state["about_tab_hidden"] = False
        if tab_state["summary_btn_clicks"] != num_summary_clicks:
            tab_state["summary_tab_hidden"] = False
        elif tab_state["diurnality_btn_clicks"] != num_diurnality_clicks:
            tab_state["diurnality_tab_hidden"] = False
        elif tab_state["individuality_btn_clicks"] != num_individuality_clicks:
            tab_state["individuality_tab_hidden"] = False

        tab_state["about_btn_clicks"] = num_about_clicks
        tab_state["summary_btn_clicks"] = num_summary_clicks
        tab_state["diurnality_btn_clicks"] = num_diurnality_clicks
        tab_state["individuality_btn_clicks"] = num_individuality_clicks

        return tab_state
