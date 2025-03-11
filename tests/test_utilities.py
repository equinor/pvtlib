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

