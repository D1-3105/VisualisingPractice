import pytest
from numpy import matrix
from core.graph_work.grapher import find_city


@pytest.fixture
def graph_matrix():
    return matrix([
        [1, 2, 3, 0, 2],
        [2, 0, 4, 2, 3],
        [3, 1, 0, 2, 1],
        [0, 2, 2, 0, 4],
        [2, 3, 1, 4, 0]
    ])


@pytest.fixture
def city_names():
    return 'SPB', 'Gatchina', 'Kingisepp', 'Kirishi', 'Slantsy'


def test_min_way_detection(graph_matrix, city_names):
    min_cum_way, city_indices, cum_weights = find_city(graph_matrix, city_names)
    assert min_cum_way == 7
    assert city_names[city_indices[0]] == city_names[2]
