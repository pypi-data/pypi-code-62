import os
import igraph
from myutils import geo

R = 6371000

##########################################################
def add_lengths(g):
    """Add length to the edges, assuming each vertex has a location"""
    if 'x' in g.vertex_attributes(): x = 'x'; y = 'y';
    else: x = 'lon'; y = 'lat';

    for i, e in enumerate(g.es()):
        lon1, lat1 = float(g.vs[e.source][x]), float(g.vs[e.source][y])
        lon2, lat2 = float(g.vs[e.target][x]), float(g.vs[e.target][y])
        g.es[i]['length'] = geo.haversine(lon1, lat1, lon2, lat2)
    return g

##########################################################
def simplify_graphml(graphpath, directed=True, simplify=True):
    """Get largest connected component from @graphatph and add weights
    According to the params @undirected, @simplify, convert to
    undirected and/or remove multiple edges and self-loops.
    If the original graph has x,y attributes, we also compute the length"""

    g = igraph.Graph.Read(graphpath)
    if simplify: g.simplify(combine_edges='first')
    if not directed: g.to_undirected()
    g = g.components(mode='weak').giant()

    if ('x' in g.vertex_attributes()) or ('lon' in g.vertex_attributes()):
        g = add_lengths(g)

    return g

##########################################################
