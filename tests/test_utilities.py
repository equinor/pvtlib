import numpy as np
from pvtlib.utilities import relative_difference, calculate_deviation, calculate_relative_deviation, calculate_max_min_diffperc

def test_relative_difference():
    assert round(relative_difference(10, 5),10)== 66.6666666667
    assert round(relative_difference(5, 10),10)== -66.6666666667
    assert np.isnan(relative_difference(0, 0))

def test_calculate_deviation():
    assert calculate_deviation(10, 5) == 5
    assert calculate_deviation(5, 10) == -5
    assert calculate_deviation(0, 0) == 0

def test_calculate_relative_deviation():
    assert calculate_relative_deviation(10, 5) == 100.0
    assert calculate_relative_deviation(5, 10) == -50.0
    assert np.isnan(calculate_relative_deviation(10, 0))

def test_calculate_max_min_diffperc():
    assert calculate_max_min_diffperc([1, 2, 3, 4, 5]) == 133.33333333333334
    assert calculate_max_min_diffperc([5, 5, 5, 5, 5]) == 0.0
    assert np.isnan(calculate_max_min_diffperc([0, 0, 0, 0, 0]))

