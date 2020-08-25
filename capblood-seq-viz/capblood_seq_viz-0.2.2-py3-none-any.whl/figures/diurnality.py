import plotly.graph_objs as graph_objects

import numpy

from capblood_seq import config

from ..data import diurnality


def get_gene_AM_PM_box_plot(gene):

    AM_PM_data = diurnality.get_gene_AM_PM_values(gene)

    AM_box_trace = graph_objects.Box(
        x=AM_PM_data["AM_mean_groups"],
        y=AM_PM_data["AM_means"],
        line={
            "color": config.AM_COLOR
        },
        name="AM"
    )

    AM_scatter_trace = graph_objects.Scatter(
        x=AM_PM_data["AM_mean_groups_jittered"],
        y=AM_PM_data["AM_means"],
        marker_color=AM_PM_data["AM_colors"],
        mode="markers",
        showlegend=False,
        name="AM"
    )

    PM_box_trace = graph_objects.Box(
        x=AM_PM_data["PM_mean_groups"],
        y=AM_PM_data["PM_means"],
        line={
            "color": config.PM_COLOR
        },
        name="PM"
    )

    PM_scatter_trace = graph_objects.Scatter(
        x=AM_PM_data["PM_mean_groups_jittered"],
        y=AM_PM_data["PM_means"],
        marker_color=AM_PM_data["PM_colors"],
        mode="markers",
        showlegend=False,
        name="PM"
    )

    title = "Mean Abundance<BR>(Normalized Within Subjects)"

    y_max = max(
        numpy.abs(AM_PM_data["PM_means"]).max(),
        numpy.abs(AM_PM_data["AM_means"]).max()
    ) * 1.1
    y_min = -y_max

    layout = graph_objects.Layout(
        {
            "yaxis": {
                "range": [y_min, y_max],
                "title": title,
                "exponentformat": "e"
            },
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "title": {
                "text": "%s Time-of-Day Expression" % gene,
                "xanchor": "center",
                "xref": "container",
                "x": 0.5
            },
            "boxmode": "group",
            "xaxis": {
                "tickvals": list(range(
                    len(AM_PM_data["cell_type_label_list"]))),
                "ticktext": AM_PM_data["cell_type_label_list"]
            }
        }
    )

    figure = graph_objects.Figure(
        data=[AM_box_trace, AM_scatter_trace, PM_box_trace, PM_scatter_trace],
        layout=layout)

    for cell_type_index, cell_type_label in \
            enumerate(AM_PM_data["cell_type_label_list"]):
        significance_line = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index - 0.175,
            x1=cell_type_index + 0.175,
            y0=y_max,
            y1=y_max,
            line=dict(
                color="Black",
                width=5
            )
        )

        significance_bracket_left = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index - 0.175,
            x1=cell_type_index - 0.175,
            y0=y_max,
            y1=y_max * 0.95,
            line=dict(
                color="Black",
                width=4
            )
        )

        significance_bracket_right = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index + 0.175,
            x1=cell_type_index + 0.175,
            y0=y_max,
            y1=y_max * 0.95,
            line=dict(
                color="Black",
                width=4
            )
        )

        figure.add_shape(significance_line)
        figure.add_shape(significance_bracket_left)
        figure.add_shape(significance_bracket_right)

        figure.add_annotation(
            graph_objects.layout.Annotation(
                text="p=%.1e" % AM_PM_data["p_values"][cell_type_index],
                showarrow=False,
                yanchor="bottom",
                yref="y",
                y=y_max,
                x=cell_type_index,
                xref="x",
                xanchor="center"
            )
        )

    return figure


def get_diurnality_figure(threshold=None):

    diurnality_df = diurnality.get_gene_diurnality()

    colors = [config.CELL_TYPE_COLORS[cell_type] for
              cell_type in diurnality_df["Max Cell Type"]]

    scatter = graph_objects.Scattergl(
        x=diurnality_df["Population Wide Z Score"],
        y=diurnality_df["By Cell Type Z Score"],
        mode="markers",
        marker={
            "size": 2+diurnality_df["Percent Cells Expressing"]*7,
            "color": colors
        },
        text=diurnality_df.index.values
    )

    figure = graph_objects.Figure(
        data=[scatter],
        layout=graph_objects.Layout(
            title="Gene Diurnality",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            paper_bgcolor="rgba(255, 255, 255, 0)",
            yaxis={
                "title": "Cell Type Z-score"
            },
            xaxis={
                "title": "Population Z-score"
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

            data = diurnality.get_gene_trace(gene, cell_type, subject_id)

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
            layout[y_axis_long_name]["title"] = "Mean Abundance<BR>" \
                "(Normalized within subjects)"

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
