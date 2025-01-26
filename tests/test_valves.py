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