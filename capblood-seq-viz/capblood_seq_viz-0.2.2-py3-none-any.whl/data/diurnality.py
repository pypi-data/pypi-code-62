import os
import pickle

import pandas

import capblood_seq

GENE_DIURNALITY_DF = None
GENE_OPTIONS = None
GENE_AM_PM_MEANS = None
GENE_MEAN_TRACES = None


def load_gene_diurnality():

    global GENE_DIURNALITY_DF
    global GENE_AM_PM_MEANS
    global GENE_MEAN_TRACES

    if GENE_DIURNALITY_DF is None:
        GENE_DIURNALITY_DF = pandas.read_csv(
            os.path.join(
                capblood_seq.get_dataset().data_directory,
                "gene_diurnality_scores.csv"
            ),
            index_col=0,
            header=[0]
        )

        pickle_file_path = os.path.join(
            capblood_seq.get_dataset().data_directory,
            "gene_AM_PM_means_subject_normalized.pickle"
        )

        with open(pickle_file_path, "rb") as pickle_file:
            GENE_AM_PM_MEANS = pickle.load(pickle_file)

        pickle_file_path = os.path.join(
            capblood_seq.get_dataset().data_directory,
            "gene_mean_traces_subject_normalized.pickle"
        )

        with open(pickle_file_path, "rb") as pickle_file:
            GENE_MEAN_TRACES = pickle.load(pickle_file)


def get_gene_options():

    load_gene_diurnality()

    global GENE_OPTIONS

    if GENE_OPTIONS is None:
        GENE_OPTIONS = sorted(GENE_DIURNALITY_DF.index.values)

        GENE_OPTIONS = [{"label": gene, "value": gene} for gene in GENE_OPTIONS]

    return GENE_OPTIONS


def get_gene_diurnality():

    load_gene_diurnality()

    return GENE_DIURNALITY_DF


def get_gene_AM_PM_values(gene):

    load_gene_diurnality()

    return GENE_AM_PM_MEANS[gene]


def get_gene_trace(gene, cell_type, subject):

    load_gene_diurnality()

    return GENE_MEAN_TRACES[gene][cell_type][subject]
