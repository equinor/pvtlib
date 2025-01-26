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

import math
from pvtlib.equipment.valves import Kv, Q_from_Kv

def test_Kv_positive_values():
    Q = 10
    SG = 1
    dP = 2
    expected = Q * math.sqrt(SG / dP)
    assert Kv(Q, SG, dP) == expected

def test_Kv_zero_dP():
    Q = 10
    SG = 1
    dP = 0
    assert math.isnan(Kv(Q, SG, dP))

def test_Kv_negative_dP():
    Q = 10
    SG = 1
    dP = -2
    assert math.isnan(Kv(Q, SG, dP))

def test_Kv_zero_SG():
    Q = 10
    SG = 0
    dP = 2
    expected = Q * math.sqrt(SG / dP)
    assert Kv(Q, SG, dP) == expected

def test_Q_from_Kv_positive_values():
    Kv_value = 10
    SG = 1
    dP = 2
    expected = Kv_value / math.sqrt(SG / dP)
    assert Q_from_Kv(Kv_value, SG, dP) == expected

def test_Q_from_Kv_zero_dP():
    Kv_value = 10
    SG = 1
    dP = 0
    assert math.isnan(Q_from_Kv(Kv_value, SG, dP))

def test_Q_from_Kv_negative_dP():
    Kv_value = 10
    SG = 1
    dP = -2
    assert math.isnan(Q_from_Kv(Kv_value, SG, dP))

def test_Q_from_Kv_zero_SG():
    Kv_value = 10
    SG = 0
    dP = 2

    assert math.isnan(Q_from_Kv(Kv_value, SG, dP))