import os
import csv

import capblood_seq


def get_cell_type_labels_counts():

    cell_count_labels = []

    cell_counts_file_path = os.path.join(
        capblood_seq.get_dataset().data_directory,
        "cell_counts.csv"
    )

    with open(cell_counts_file_path, "r", newline="") as cell_counts_file:
        cell_counts_file = csv.reader(cell_counts_file, delimiter=",")
        for line in cell_counts_file:
            cell_count_labels.append(line)

    return cell_count_labels
