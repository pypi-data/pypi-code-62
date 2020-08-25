import pickle
from bioservices.kegg import KEGG
k = KEGG()

import pandas
from statsmodels.stats import proportion

from capblood_seq import common
from capblood_seq import resources
from capblood_seq import config

from . import diurnality as diurnality_data
from . import individuality as individuality_data

GENE_PATHWAY_DICT = None
PATHWAY_CLASS_LABELS = None
PATHWAY_CLASSES = None
PATHWAY_ENRICHMENT_BY_THRESHOLD = None


def load_pathway_data():

    global GENE_PATHWAY_DICT
    global PATHWAY_CLASS_LABELS
    global PATHWAY_CLASSES
    global PATHWAY_ENRICHMENT_BY_THRESHOLD

    if GENE_PATHWAY_DICT is None:
        GENE_PATHWAY_DICT = pickle.load(
            open(common.get_resource_path(
                resources, "gene_pathway_dict.pickle"
            ), "rb")
        )

        with open(common.get_resource_path(
                resources, "pathway_class_labels.tsv"), "r") as \
                pathway_class_labels_file:

            PATHWAY_CLASS_LABELS = {}

            pathway_class_labels_file.readline()
            for line in pathway_class_labels_file.readlines():
                line = line.strip()
                pathway_class_label = line.split("\t")
                PATHWAY_CLASS_LABELS[pathway_class_label[0]] = \
                    pathway_class_label[1]

        pathway_class_df = pandas.read_csv(
            common.get_resource_path(resources, "pathway_classes.csv"),
            index_col=0, header=0)

        PATHWAY_CLASSES = {}

        for row in pathway_class_df.iterrows():
            pathway = row[0]
            PATHWAY_CLASSES[pathway] = row[1][1]

        PATHWAY_ENRICHMENT_BY_THRESHOLD = {}


def get_pathway(gene):

    global GENE_PATHWAY_DICT

    if gene in GENE_PATHWAY_DICT:
        return GENE_PATHWAY_DICT[gene]
    else:
        GENE_PATHWAY_DICT[gene] = k.get_pathway_by_gene(gene, "hsa")


def get_pathway_enrichment(num_top_genes=250):

    load_pathway_data()

    global PATHWAY_CLASS_LABELS
    global PATHWAY_CLASSES
    global PATHWAY_ENRICHMENT_BY_THRESHOLD

    if num_top_genes in PATHWAY_ENRICHMENT_BY_THRESHOLD:
        return PATHWAY_ENRICHMENT_BY_THRESHOLD[num_top_genes]

    diurnality_df = diurnality_data.get_gene_diurnality()
    diurnality_df = diurnality_df.sort_values(by="By Cell Type p-value")
    individuality_df = individuality_data.get_gene_individuality()
    individuality_df = individuality_df.sort_values(by="By Cell Type p-value")

    pathway_set = set()

    diurnal_pathway_counts = {}
    diurnal_label_counts = {}
    nondiurnal_pathway_counts = {}
    nondiurnal_label_counts = {}
    individual_pathway_counts = {}
    individual_label_counts = {}
    nonindividual_pathway_counts = {}
    nonindividual_label_counts = {}

    for gene_index, gene in enumerate(diurnality_df.index.values):

        pathways = get_pathway(gene)

        if pathways is None:
            continue

        pathway_count = 1/len(pathways)

        for pathway_id, pathway in pathways.items():
            pathway_set.add(pathway)
            pathway_class = PATHWAY_CLASSES[pathway]
            pathway_label = PATHWAY_CLASS_LABELS[pathway_class]
            if gene_index < num_top_genes:
                if pathway not in diurnal_pathway_counts:
                    diurnal_pathway_counts[pathway] = 0
                diurnal_pathway_counts[pathway] += pathway_count
                if pathway_label not in diurnal_label_counts:
                    diurnal_label_counts[pathway_label] = 0
                diurnal_label_counts[pathway_label] += pathway_count
            else:
                if pathway not in nondiurnal_pathway_counts:
                    nondiurnal_pathway_counts[pathway] = 0
                nondiurnal_pathway_counts[pathway] += pathway_count
                if pathway_label not in nondiurnal_label_counts:
                    nondiurnal_label_counts[pathway_label] = 0
                nondiurnal_label_counts[pathway_label] += pathway_count

    for gene_index, gene in enumerate(individuality_df.index.values):

        pathways = get_pathway(gene)

        if pathways is None:
            continue

        pathway_count = 1 / len(pathways)

        for pathway_id, pathway in pathways.items():
            pathway_set.add(pathway)
            pathway_class = PATHWAY_CLASSES[pathway]
            pathway_label = PATHWAY_CLASS_LABELS[pathway_class]
            if gene_index < num_top_genes:
                if pathway not in individual_pathway_counts:
                    individual_pathway_counts[pathway] = 0
                individual_pathway_counts[pathway] += pathway_count
                if pathway_label not in individual_label_counts:
                    individual_label_counts[pathway_label] = 0
                individual_label_counts[pathway_label] += pathway_count
            else:
                if pathway not in nonindividual_pathway_counts:
                    nonindividual_pathway_counts[pathway] = 0
                nonindividual_pathway_counts[pathway] += pathway_count
                if pathway_label not in nonindividual_label_counts:
                    nonindividual_label_counts[pathway_label] = 0
                nonindividual_label_counts[pathway_label] += pathway_count

    pathway_list = []
    pathway_diurnal_enrichments = []
    pathway_individual_enrichments = []

    for pathway in pathway_set:

        if pathway not in diurnal_pathway_counts or pathway not in \
                nondiurnal_pathway_counts or pathway not in \
                individual_pathway_counts or pathway not in \
                nonindividual_pathway_counts:
            continue

        pathway_list.append(pathway)

        diurnal_enrichment, diurnal_p = proportion.proportions_ztest(
            [
                diurnal_pathway_counts[pathway],
                nondiurnal_pathway_counts[pathway]
            ],
            [
                sum(diurnal_pathway_counts.values()),
                sum(nondiurnal_pathway_counts.values())
            ]
        )

        individual_enrichment, individual_p = proportion.proportions_ztest(
            [
                individual_pathway_counts[pathway],
                nonindividual_pathway_counts[pathway]
            ],
            [
                sum(individual_pathway_counts.values()),
                sum(nonindividual_pathway_counts.values())
            ]
        )

        pathway_diurnal_enrichments.append(diurnal_enrichment)
        pathway_individual_enrichments.append(individual_enrichment)

    pathway_label_data = {}

    for class_index, class_label in enumerate(config.PATHWAY_LABELS):

        x_values = []
        y_values = []
        text_labels = []

        for pathway_index, pathway in enumerate(pathway_list):
            pathway_class = PATHWAY_CLASSES[pathway]
            pathway_label = PATHWAY_CLASS_LABELS[pathway_class]
            if pathway_label == class_label:
                x_values.append(pathway_individual_enrichments[pathway_index])
                y_values.append(pathway_diurnal_enrichments[pathway_index])
                text_labels.append(pathway)

        individual_enrichment, _ = proportion.proportions_ztest(
            [
                individual_label_counts[class_label],
                nonindividual_label_counts[class_label]
            ],
            [
                sum(individual_label_counts.values()),
                sum(nonindividual_label_counts.values())
            ]
        )

        diurnal_enrichment, _ = proportion.proportions_ztest(
            [
                diurnal_label_counts[class_label],
                nondiurnal_label_counts[class_label]
            ],
            [
                sum(diurnal_label_counts.values()),
                sum(nondiurnal_label_counts.values())
            ]
        )

        x_values.append(individual_enrichment)
        y_values.append(diurnal_enrichment)
        text_labels.append(class_label)

        pathway_label_data[class_label] = {
            "x_values": x_values,
            "y_values": y_values,
            "text_labels": text_labels
        }

    PATHWAY_ENRICHMENT_BY_THRESHOLD[num_top_genes] = pathway_label_data

    return pathway_label_data
