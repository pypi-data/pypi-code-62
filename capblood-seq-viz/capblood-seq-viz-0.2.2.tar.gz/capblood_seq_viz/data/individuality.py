import os
import pickle

import pandas

import capblood_seq

GENE_INDIVIDUALITY_DF = None
GENE_OPTIONS = None
GENE_MEAN_TRACES = None


def load_gene_individuality():

    global GENE_INDIVIDUALITY_DF
    global GENE_MEAN_TRACES

    if GENE_INDIVIDUALITY_DF is None:
        GENE_INDIVIDUALITY_DF = pandas.read_csv(
            os.path.join(
                capblood_seq.get_dataset().data_directory,
                "gene_individuality_scores.csv"
            ),
            index_col=0,
            header=[0]
        )

        pickle_file_path = os.path.join(
            capblood_seq.get_dataset().data_directory,
            "gene_mean_traces.pickle"
        )

        with open(pickle_file_path, "rb") as pickle_file:
            GENE_MEAN_TRACES = pickle.load(pickle_file)


def get_gene_options():

    load_gene_individuality()

    global GENE_OPTIONS

    if GENE_OPTIONS is None:
        GENE_OPTIONS = sorted(GENE_INDIVIDUALITY_DF.index.values)

        GENE_OPTIONS = [{"label": gene, "value": gene} for gene in GENE_OPTIONS]

    return GENE_OPTIONS


def get_gene_individuality():

    load_gene_individuality()

    return GENE_INDIVIDUALITY_DF


def get_gene_trace(gene, cell_type, subject):

    load_gene_individuality()

    return GENE_MEAN_TRACES[gene][cell_type][subject]
