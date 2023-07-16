import pytest
from core.graph_work.tests import graph_matrix, city_names
from core.graph_work.grapher import Graph


@pytest.fixture
def graph(graph_matrix, city_names):
    graph = Graph(graph_matrix, city_names)
    return graph
