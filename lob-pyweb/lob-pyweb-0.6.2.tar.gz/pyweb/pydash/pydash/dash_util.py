import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from urllib.parse import quote


def dropdown(options, id):
    return dcc.Dropdown(
            id=id, options=[{'label': name, 'value': name} for name in options],
            value=options[0], clearable=False, multi=False,  searchable=True
        )


def dropdown_multi(options, id):
    return dcc.Dropdown(
            id = id, options=[{'label': name, 'value': name} for name in options],
            multi=True, searchable=True
    )
 

def frame2lines(frame):   
    return [go.Scatter(x=frame[col].dropna().index, y=frame[col].dropna().values, mode="lines", name=col, showlegend=True) for col in frame]
   

def year_slider(minyear, maxyear):
        return dcc.RangeSlider(
            id='year-slider', min=minyear, max=maxyear, value=[minyear, maxyear],
            marks={str(year): str(year) for year in range(minyear, maxyear + 1)},
            step=None
        )


def frame2href(frame):
    csv_string = frame.to_csv(encoding='utf-8')
    return "data:text/csv;charset=utf-8," + quote(csv_string)


def frame2table(frame):
    df = frame.reset_index()
    if df.empty:
        return [], []
    else:
        return [{"name": i, "id": i} for i in df.columns], df.to_dict('records')

