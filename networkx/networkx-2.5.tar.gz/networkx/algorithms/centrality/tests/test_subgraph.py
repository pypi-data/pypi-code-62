import pytest

numpy = pytest.importorskip("numpy")
scipy = pytest.importorskip("scipy")

import networkx as nx
from networkx.algorithms.centrality.subgraph_alg import (
    estrada_index,
    communicability_betweenness_centrality,
    subgraph_centrality,
    subgraph_centrality_exp,
)
from networkx.testing import almost_equal


class TestSubgraph:
    def test_subgraph_centrality(self):
        answer = {0: 1.5430806348152433, 1: 1.5430806348152433}
        result = subgraph_centrality(nx.path_graph(2))
        for k, v in result.items():
            assert almost_equal(answer[k], result[k], places=7)

        answer1 = {
            "1": 1.6445956054135658,
            "Albert": 2.4368257358712189,
            "Aric": 2.4368257358712193,
            "Dan": 3.1306328496328168,
            "Franck": 2.3876142275231915,
        }
        G1 = nx.Graph(
            [
                ("Franck", "Aric"),
                ("Aric", "Dan"),
                ("Dan", "Albert"),
                ("Albert", "Franck"),
                ("Dan", "1"),
                ("Franck", "Albert"),
            ]
        )
        result1 = subgraph_centrality(G1)
        for k, v in result1.items():
            assert almost_equal(answer1[k], result1[k], places=7)
        result1 = subgraph_centrality_exp(G1)
        for k, v in result1.items():
            assert almost_equal(answer1[k], result1[k], places=7)

    def test_subgraph_centrality_big_graph(self):
        g199 = nx.complete_graph(199)
        g200 = nx.complete_graph(200)

        comm199 = nx.subgraph_centrality(g199)
        comm199_exp = nx.subgraph_centrality_exp(g199)

        comm200 = nx.subgraph_centrality(g200)
        comm200_exp = nx.subgraph_centrality_exp(g200)

    def test_communicability_betweenness_centrality(self):
        answer = {
            0: 0.07017447951484615,
            1: 0.71565598701107991,
            2: 0.71565598701107991,
            3: 0.07017447951484615,
        }
        result = communicability_betweenness_centrality(nx.path_graph(4))
        for k, v in result.items():
            assert almost_equal(answer[k], result[k], places=7)

        answer1 = {
            "1": 0.060039074193949521,
            "Albert": 0.315470761661372,
            "Aric": 0.31547076166137211,
            "Dan": 0.68297778678316201,
            "Franck": 0.21977926617449497,
        }
        G1 = nx.Graph(
            [
                ("Franck", "Aric"),
                ("Aric", "Dan"),
                ("Dan", "Albert"),
                ("Albert", "Franck"),
                ("Dan", "1"),
                ("Franck", "Albert"),
            ]
        )
        result1 = communicability_betweenness_centrality(G1)
        for k, v in result1.items():
            assert almost_equal(answer1[k], result1[k], places=7)

    def test_estrada_index(self):
        answer = 1041.2470334195475
        result = estrada_index(nx.karate_club_graph())
        assert almost_equal(answer, result, places=7)
