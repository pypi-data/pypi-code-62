import pathlib
import sys

from bokeh.events import Event

ROOT_PATH = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_PATH))

from typing import Type

import panel as pn
import param
from panel.viewable import Viewable

from derobertis_project_logo.logo import Logo
from derobertis_project_logo.triangle import Triangle


class LogoModel(param.Parameterized):
    klass: Type[Logo] = param.ObjectSelector(objects=[Triangle])
    instance: Logo = param.ClassSelector(class_=Logo)
    project_name: str = param.String(default='my_project')

    def __init__(self, **params):
        if 'instance' not in params:
            t = Triangle()
            t.set_random_colors()
            params['instance'] = t
        super().__init__(**params)

    def _repr_svg_(self) -> str:
        return self.instance.render_str()


def get_view() -> Viewable:
    logo_model = LogoModel()
    svg = pn.pane.SVG(object=logo_model)
    editor = pn.widgets.Ace(
        value=logo_model.instance.to_definition(logo_model.project_name),
        width=500
    )

    def randomize_color(event: Event):
        logo_model.instance.set_random_colors()
        svg.object = logo_model
        editor.value = logo_model.instance.to_definition(logo_model.project_name)

    random_colors_button = pn.widgets.Button(name='Randomize Colors')
    random_colors_button.on_click(randomize_color)

    # logo_model.link(svg, instance='object')

    return pn.Column(
        pn.Row(logo_model.param, editor),
        random_colors_button,
        svg
    )

get_view().servable()