import pytest
import numpy as np
from core.heli.poly import is_line_inside, make_quadro_corners


@pytest.fixture
def line_params():
    return 12 / 8, 0


@pytest.fixture
def q_params():
    return 2, 2, float(4 * np.sqrt(2))


def test_line_is_sepa(line_params, q_params):
    res = is_line_inside(*line_params, *q_params)
    assert res is True


def test_quadro_params_creation():
    poly_params, d = make_quadro_corners(2, 3, 4)


def test_line_is_sepa_real_data():
    quadro_params, d = make_quadro_corners(2, 3, 4)
    results = []
    for q_r in quadro_params:
        for q_col in q_r:
            results.append(
                is_line_inside(12 / 8, 0, *q_col, d=d)
            )
    assert results.count(True) == 4
