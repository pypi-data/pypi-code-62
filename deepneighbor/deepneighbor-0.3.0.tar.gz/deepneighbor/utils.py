import networkx as nx
import itertools
import random
import pandas as pd


def generate_sentences(data):
    '''
    input dataframe.
      user  item
    	1	a
    	1	b
    	1	c
    	2	d
    	2	a
    output sentences. [user_id1, all_item(1...k1),user_id2,all_item(1...k2),...]
    [1,a,b,c,2,d,a]
    '''
    sentences = []

    edges = data.values.tolist()
    edges = [[int(edge[0]), int(edge[1])] for edge in edges]
    graph = nx.from_edgelist(edges)
    graph.remove_edges_from(nx.selfloop_edges(graph))

    for node in graph.nodes():
        temp = []
        temp = [str(node)] + [str(n) for n in list(graph.neighbors(node))]
        sentences.append(temp)
    return graph, sentences

def convert_to(data,le):
    '''
    given txt or csv file
    transform with label encoder
    return dataframe with two columns [from] and [to]
    '''

    data = pd.read_csv(data)
    data.columns = ['user','item']
    le.fit(data.user.unique().tolist()+data.item.unique().tolist())
    for col in data.columns:
        data[col] = le.transform(data[col])
    return data,le




def generate_sentences_dw(data):
    return nx.read_edgelist(data,)
