"""Reading and writing data."""

import numpy as np
import pandas as pd
import networkx as nx
from tqdm import tqdm
from scipy import sparse
#from texttable import Texttable
from sklearn import preprocessing

def read_graph(data):
    """
    Method to read graph and create a target matrix with pooled adjacency matrix powers.
    :param args: Arguments object.
    :return graph: graph.
    """
    print("\nTarget matrix creation started.\n")
    edges = data.values.tolist()
    edges = [[int(edge[0]), int(edge[1])] for edge in edges]
    graph = nx.from_edgelist(edges)
    graph.remove_edges_from(nx.selfloop_edges(graph))
    return graph



# def tab_printer(args):
#     """
#     Function to print the logs in a nice tabular format.
#     :param args: Parameters used for the model.
#     """
#     args = vars(args)
#     keys = sorted(args.keys())
#     t = Texttable()
#     t.add_rows([["Parameter", "Value"]])
#     t.add_rows([[k.replace("_", " ").capitalize(), args[k]] for k in keys])
#     print(t.draw())

def feature_calculator( graph,window_size):
    """
    Calculating the feature tensor.
    :param args: Arguments object.
    :param graph: NetworkX graph.
    :return target_matrices: Target tensor.
    """
    index_1 = [edge[0] for edge in graph.edges()] + [edge[1] for edge in graph.edges()]
    index_2 = [edge[1] for edge in graph.edges()] + [edge[0] for edge in graph.edges()]
    values = [1 for edge in index_1]
    node_count = max(len(set(index_1)), len(set(index_2)))
    adjacency_matrix = sparse.coo_matrix((values, (index_1, index_2)),
                                         shape=(node_count, node_count),
                                         dtype=np.float32)

    degrees = adjacency_matrix.sum(axis=0)[0].tolist()
    degs = sparse.diags(degrees, [0])
    normalized_adjacency_matrix = degs.dot(adjacency_matrix)
    target_matrices = [normalized_adjacency_matrix.todense()]
    powered_A = normalized_adjacency_matrix
    if window_size > 1:
        for power in tqdm(range(window_size-1), desc="Adjacency matrix powers"):
            powered_A = powered_A.dot(normalized_adjacency_matrix)
            to_add = powered_A.todense()
            target_matrices.append(to_add)
    target_matrices = np.array(target_matrices)
    #print(target_matrices)
    return target_matrices

def adjacency_opposite_calculator(graph):
    """
    Creating no edge indicator matrix.
    :param graph: NetworkX object.
    :return adjacency_matrix_opposite: Indicator matrix.
    """
    adjacency_matrix = sparse.csr_matrix(nx.adjacency_matrix(graph), dtype=np.float32).todense()
    adjacency_matrix_opposite = np.ones(adjacency_matrix.shape) - adjacency_matrix
    return adjacency_matrix_opposite
