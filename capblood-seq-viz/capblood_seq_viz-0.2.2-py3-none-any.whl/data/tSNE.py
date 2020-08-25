import os
from enum import Enum

import pandas

import capblood_seq


class Cell_Grouping(Enum):

    NONE = 0
    CELL_TYPE = 1
    SUBJECT = 2
    GENDER = 3
    SAMPLE = 4
    TIME_OF_DAY = 5

    def to_name(self):
        return CELL_GROUPING_NAMES[self]


CELL_GROUPING_NAMES = {
    Cell_Grouping.NONE: None,
    Cell_Grouping.CELL_TYPE: "Cell Type",
    Cell_Grouping.SUBJECT: "Subject",
    Cell_Grouping.GENDER: "Gender",
    Cell_Grouping.SAMPLE: "Sample",
    Cell_Grouping.TIME_OF_DAY: "Time of Day"
}

CELL_GROUPING_COLUMN_NAMES = {
    Cell_Grouping.NONE: None,
    Cell_Grouping.CELL_TYPE: "Cell Type(s)",
    Cell_Grouping.SUBJECT: "Subject ID",
    Cell_Grouping.GENDER: "Gender",
    Cell_Grouping.SAMPLE: "Sample",
    Cell_Grouping.TIME_OF_DAY: "Time of Day"
}

# The global cell coordinate data frame
cell_metadata = None
cell_coordinates_by_group = {}


def load_cell_metadata():

    global cell_metadata

    if cell_metadata is None:

        cell_metadata_file_path = os.path.join(
            capblood_seq.get_dataset().data_directory,
            "cell_tSNE_coordinates_metadata.csv"
        )

        if not os.path.exists(cell_metadata_file_path):
            raise ValueError("Data does not exist, please download")

        cell_metadata = pandas.read_csv(cell_metadata_file_path, header=0)


def load_cell_coordinates_by_group(group_by=Cell_Grouping.SUBJECT):

    column_name = CELL_GROUPING_COLUMN_NAMES[group_by]

    load_cell_metadata()

    cell_coordinates = cell_metadata[["t-SNE x", "t-SNE y"]]

    global cell_coordinates_by_group

    if group_by == Cell_Grouping.NONE:
        cell_coordinates_by_group[group_by] = cell_coordinates
    elif group_by == Cell_Grouping.CELL_TYPE:

        cell_coordinates_by_group[group_by] = {}

        cell_type_strings = cell_metadata[column_name].unique()

        cell_types = set()

        for cell_type_string in cell_type_strings:

            if pandas.isnull(cell_type_string):
                continue

            cell_types.update(cell_type_string.split(";"))

        cell_types = list(sorted(cell_types))

        for cell_type in cell_types:

            if pandas.isnull(cell_type):
                cell_coordinates_by_group[group_by][None] = \
                    cell_coordinates[
                        cell_metadata[column_name].isnull()
                    ].values
            else:
                cell_coordinates_by_group[group_by][cell_type] = \
                    cell_coordinates[
                        (~cell_metadata[column_name].isnull()) &
                        (cell_metadata[column_name].str.contains(cell_type))
                    ].values
    else:

        cell_coordinates_by_group[group_by] = {}

        groups = cell_metadata[column_name].unique()

        for group in groups:

            if pandas.isnull(group):
                cell_coordinates_by_group[group_by][None] = \
                    cell_coordinates[
                        cell_metadata[column_name].isnull()
                    ].values
            else:
                cell_coordinates_by_group[group_by][group] = \
                    cell_coordinates[
                        cell_metadata[column_name] == group
                    ].values


def get_cell_coordinates(group_by=Cell_Grouping.SUBJECT):

    if group_by not in cell_coordinates_by_group:
        load_cell_coordinates_by_group(group_by)

    return cell_coordinates_by_group[group_by]
