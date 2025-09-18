"""MIT License

Copyright (c) 2025 Christian Hågenvik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
from pvtlib.utilities import linear_interpolation, relative_difference, calculate_deviation, calculate_relative_deviation, calculate_max_min_diffperc

def test_linear_interpolation():
    X = [100, 300, 900, 1400, 1900, 2500, 3100]
    Y = [-0.09, -0.05, 0.1, 0.15, 0.16, 0.14, 0.05]

    testdata = {
        'test1' : {'x': 0, 'expected': -0.09},
        'test2' : {'x': 150, 'expected': -0.08},
        'test3' : {'x': 200, 'expected': -0.07},
        'test4' : {'x': 500, 'expected': 0.00},
        'test5' : {'x': 1000, 'expected': 0.11},
        'test6' : {'x': 1500, 'expected': 0.152},
        'test7' : {'x': 2000, 'expected': 0.1566666667},
        'test8' : {'x': 2500, 'expected': 0.14},
        'test9' : {'x': 3000, 'expected': 0.065},
        'test10' : {'x': 3500, 'expected': 0.05},
    }
    
    for key, value in testdata.items():
        x = value['x']
        expected = value['expected']
        result = linear_interpolation(x, X, Y)
        assert round(result, 10) == expected, f"Test {key} failed: expected {expected}, got {result}"

def test_linear_interpolation_invalid_inputs():
    # Test when x is nan, should return nan
    X = [100, 300, 900, 1400, 1900, 2500, 3100]
    Y = [-0.09, -0.05, 0.1, 0.15, 0.16, 0.14, 0.05]
    result = linear_interpolation(np.nan, X, Y)
    assert np.isnan(result), "Expected nan when x is nan"

    # Test when x_values and y_values are not the same length, should raise ValueError
    X_short = [100, 300, 900]
    Y_long = [-0.09, -0.05, 0.1, 0.15]
    try:
        linear_interpolation(200, X_short, Y_long)
        assert False, "Expected ValueError when x_values and y_values have different lengths"
    except ValueError as e:
        assert str(e) == "x_values and y_values must have the same length."

def test_linear_interpolation_xvalues_not_sorted():
    # Test when x_values are not in ascending order, should raise ValueError
    X_unsorted = [100, 900, 300, 1400]
    Y = [-0.09, 0.1, -0.05, 0.15]
    try:
        linear_interpolation(200, X_unsorted, Y)
        assert False, "Expected ValueError when x_values are not sorted in ascending order"
    except ValueError as e:
        assert str(e) == "x_values must be sorted in ascending order."

def test_linear_interpolation_on_exact_points():
    # Test interpolation when x matches exactly an x_value
    X = [100, 300, 900]
    Y = [1.0, 2.0, 3.0]
    assert linear_interpolation(100, X, Y) == 1.0
    assert linear_interpolation(300, X, Y) == 2.0
    assert linear_interpolation(900, X, Y) == 3.0

def test_linear_interpolation_out_of_bounds():
    # Test interpolation when x is below and above the range
    X = [10, 20, 30]
    Y = [100, 200, 300]
    assert linear_interpolation(5, X, Y) == 100
    assert linear_interpolation(35, X, Y) == 300

def test_relative_difference_zero():
    # Test zero
    assert np.isnan(relative_difference(0, 0))

def test_calculate_deviation_negative():
    # Test negative values
    assert calculate_deviation(-10, -5) == -5
    assert calculate_deviation(-5, -10) == 5

def test_calculate_relative_deviation_negative():
    # Test negative reference value
    assert calculate_relative_deviation(10, -5) == -300.0
    assert calculate_relative_deviation(-10, 5) == -300.0

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

