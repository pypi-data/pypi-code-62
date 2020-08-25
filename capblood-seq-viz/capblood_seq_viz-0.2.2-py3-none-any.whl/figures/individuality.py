import numpy

import plotly.graph_objs as graph_objects

from capblood_seq import config

from ..data import individuality


def get_individuality_figure(threshold=None):

    individuality_df = individuality.get_gene_individuality()

    colors = [config.CELL_TYPE_COLORS[cell_type] for
              cell_type in individuality_df["Max Cell Type"]]

    scatter = graph_objects.Scattergl(
        x=numpy.log2(individuality_df["Cell Type F Statistic"]),
        y=numpy.log2(individuality_df["By Cell Type F Statistic"]),
        mode="markers",
        marker={
            "size": 2+individuality_df["Percent Cells Expressing"]*7,
            "color": colors
        },
        text=individuality_df.index.values
    )

    figure = graph_objects.Figure(
        data=[scatter],
        layout=graph_objects.Layout(
            title="Gene Individuality",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            paper_bgcolor="rgba(255, 255, 255, 0)",
            yaxis={
                "title": "Subject Specificity F-statistic (log2)"
            },
            xaxis={
                "title": "Cell Type Specificity F-statistic (log2)"
            }
        )
    )

    return figure


def get_gene_traces(gene):

    traces = []
    layout = {}

    cell_types = config.CELL_TYPES + [None]
    num_cell_types = len(cell_types)

    x_axis_index = 1
    x_axis_short_name = "x"
    x_axis_long_name = "xaxis"
    y_axis_index = 1
    y_axis_short_name = "y"
    y_axis_long_name = "yaxis"
    column_start_x = 0
    column_spacing = 0.05
    column_width = (1-((num_cell_types - 1)*column_spacing))/num_cell_types

    for cell_type_index, cell_type in enumerate(cell_types):

        cell_type_label = cell_type
        if cell_type_label is None:
            cell_type_label = "All Cells"

        for subject_id in config.SUBJECT_IDS:

            data = individuality.get_gene_trace(gene, cell_type, subject_id)

            color = config.SUBJECT_ID_COLORS[subject_id]
            error_color = color.replace("1.00)", "0.50)")

            scatter = graph_objects.Scatter(
                x=data["x_values"],
                y=data["y_values"],
                error_y={
                    "array": data["errors"],
                    "color": error_color,
                    "thickness": 1.5
                },
                name=subject_id,
                line={
                    "color": color
                },
                yaxis=y_axis_short_name,
                xaxis=x_axis_short_name,
                showlegend=cell_type_index == num_cell_types - 1
            )

            traces.append(scatter)

        layout[x_axis_long_name] = {
            "domain": [column_start_x, column_start_x+column_width],
            "anchor": y_axis_short_name,
            "title": cell_type_label
        }

        layout[y_axis_long_name] = {
            "domain": [0, 1],
            "rangemode": "tozero",
            "exponentformat": "e",
            "showexponent": "all",
            "anchor": x_axis_short_name
        }

        if cell_type_index == 0:
            layout[y_axis_long_name]["title"] = "Mean Abundance"

        x_axis_index += 1
        x_axis_short_name = "x%i" % x_axis_index
        x_axis_long_name = "xaxis%i" % x_axis_index

        y_axis_index += 1
        y_axis_short_name = "y%i" % y_axis_index
        y_axis_long_name = "yaxis%i" % y_axis_index

        column_start_x += column_width + column_spacing

    layout["plot_bgcolor"] = "rgba(255, 255, 255, 0)"
    layout["paper_bgcolor"] = "rgba(255, 255, 255, 0)"
    layout["title"] = {
        "text": "%s Expression Over Time" % gene,
        "xanchor": "center",
        "xref": "container",
        "x": 0.5
    }

    figure = graph_objects.Figure(data=traces, layout=layout)

    return figure
