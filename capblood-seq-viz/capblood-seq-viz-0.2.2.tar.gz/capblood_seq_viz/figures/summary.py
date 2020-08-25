from enum import Enum

import plotly.graph_objs as graph_objects

from capblood_seq import config

from ..common import data
from ..data import cell_counts
from ..data import pathways


def get_cell_tSNE_figure(group_by=data.Cell_Grouping.SUBJECT):

    cell_coordinates_by_group = data.get_cell_coordinates(group_by=group_by)

    traces = []

    group_names_sorted = list(sorted(
        group_name for group_name in cell_coordinates_by_group.keys()
        if group_name is not None
    ))

    if None in cell_coordinates_by_group.keys():
        group_names_sorted.append(None)

    for group_name in group_names_sorted:

        cell_coordinates = cell_coordinates_by_group[group_name]

        if group_name is None:
            group_name = "Other"

        scatter = graph_objects.Scattergl(
            x=cell_coordinates[:, 0],
            y=cell_coordinates[:, 1],
            mode="markers",
            marker={
                "size": 4
            },
            name=group_name
        )

        traces.append(scatter)

    figure = graph_objects.Figure(
        data=traces,
        layout=graph_objects.Layout(
            title="Cell Projection",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            paper_bgcolor="rgba(255, 255, 255, 0)"
        )
    )

    return figure


def get_sunburst_figure():

    cell_count_labels = cell_counts.get_cell_type_labels_counts()

    cell_types = \
        [cell_count_label[0] for cell_count_label in cell_count_labels]
    friendly_labels = \
        [cell_count_label[1] for cell_count_label in cell_count_labels]
    friendly_parent_labels = \
        [cell_count_label[2] for cell_count_label in cell_count_labels]
    cell_types_counts = \
        [cell_count_label[3] for cell_count_label in cell_count_labels]

    return {
        "data": [
            graph_objects.Sunburst(
                labels=friendly_labels,
                parents=friendly_parent_labels,
                values=cell_types_counts,
                branchvalues="total",
                leaf={"opacity": 1.0},
                marker=dict(
                    colors=[
                        config.CELL_TYPE_HIERARCHICAL_COLORS[cell_type]
                        for cell_type in cell_types
                    ]
                )
            )
        ],
        "layout": graph_objects.Layout(
            title="Cell Type Distribution",
            showlegend=False,
            autosize=True
        )
    }


def get_pathway_enrichment_figure():

    pathway_label_data = pathways.get_pathway_enrichment()

    traces = []

    for pathway_label, enrichment_data in pathway_label_data.items():

        sizes = [5]*(len(enrichment_data["x_values"]) - 1)
        sizes.append(25)

        traces.append(
            graph_objects.Scatter(
                x=enrichment_data["x_values"],
                y=enrichment_data["y_values"],
                mode="markers",
                text=enrichment_data["text_labels"],
                marker={
                    "line": {
                        "width": 1,
                        "color": "black"
                    },
                    "color": config.PATHWAY_LABEL_COLORS[pathway_label],
                    "size": sizes
                },
                opacity=0.8,
                name=pathway_label
            )
        )

    layout = graph_objects.Layout(
        title="Pathway Enrichments",
        showlegend=True,
        xaxis=dict(
            title="Subject Enrichment"),
        yaxis=dict(
            title="Diurnal Enrichment"
        ),
        hovermode="closest",
        plot_bgcolor="rgba(255, 255, 255, 0)",
        paper_bgcolor="rgba(255, 255, 255, 0)",
        legend={
            "itemsizing": "constant"
        }
    )

    figure = graph_objects.Figure(data=traces, layout=layout)

    return figure
