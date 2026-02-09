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
import pytest
from pvtlib.equipment.compressors import (
    poly_exp,
    poly_head,
    poly_eff,
    dh,
    flow_coeff,
    impeller_tang_vel,
    sigma_u_squared,
    poly_head_coeff,
    work_coefficient
)


# === Tests for poly_exp ===

def test_poly_exp():
    """Test polytropic exponent calculation from docstring example."""
    p_suction = 1.5
    p_discharge = 5.0
    rho_suction = 6.0
    rho_discharge = 12.0
    
    result = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    expected = 1.7369655941662063
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_poly_exp_all_zero_cases():
    """Test all zero-value scenarios return NaN."""
    assert np.isnan(poly_exp(0, 5.0, 6.0, 12.0)), "Zero p_suction"
    assert np.isnan(poly_exp(1.5, 0, 6.0, 12.0)), "Zero p_discharge"
    assert np.isnan(poly_exp(1.5, 5.0, 0, 12.0)), "Zero rho_suction"
    assert np.isnan(poly_exp(1.5, 5.0, 6.0, 0)), "Zero rho_discharge"


def test_poly_exp_realistic_values():
    """Test with realistic compression scenario values."""
    # Typical natural gas compression
    p_suction = 50.0  # bara
    p_discharge = 100.0  # bara
    rho_suction = 40.0  # kg/m³
    rho_discharge = 75.0  # kg/m³
    
    result = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    
    # Polytropic exponent should be between 1 and 2 for real gases
    assert 1.0 < result < 2.0, f"Unrealistic polytropic exponent: {result}"


# === Tests for poly_head ===

def test_poly_head():
    """Test polytropic head calculation from docstring example."""
    poly_exp_val = 1.36
    p_suction = 51.0
    p_discharge = 81.0
    rho_suction = 40.7
    rho_discharge = 57.1
    
    result = poly_head(poly_exp_val, p_suction, p_discharge, rho_suction, rho_discharge)
    expected = 62.51945306236031
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_poly_head_zero_density():
    """Test zero density values return NaN."""
    assert np.isnan(poly_head(1.25, 1.0, 5.0, 0, 40)), "Zero rho_suction"
    assert np.isnan(poly_head(1.25, 1.0, 5.0, 10, 0)), "Zero rho_discharge"


# === Tests for poly_eff ===

def test_poly_eff():
    """Test polytropic efficiency calculation from docstring example."""
    poly_head_val = 80.0
    dh_val = 100.0
    
    result = poly_eff(poly_head_val, dh_val)
    expected = 0.8
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_poly_eff_zero_dh():
    """Test zero enthalpy rise returns NaN."""
    assert np.isnan(poly_eff(80.0, 0)), "Zero dh"


def test_poly_eff_physical_limits():
    """Test that efficiency is between 0 and 1."""
    poly_head_val = 80.0
    dh_val = 100.0
    
    result = poly_eff(poly_head_val, dh_val)
    
    # Polytropic efficiency should be between 0 and 1
    assert 0 < result <= 1.0, f"Unrealistic efficiency: {result}"


# === Tests for dh ===

def test_dh():
    """Test specific mass enthalpy rise calculation from docstring example."""
    mass_enthalpy_1 = 100.0
    mass_enthalpy_2 = 150.0
    
    result = dh(mass_enthalpy_1, mass_enthalpy_2)
    expected = 50.0
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_dh_negative_rise():
    """Test with negative enthalpy rise (expansion)."""
    mass_enthalpy_1 = 150.0
    mass_enthalpy_2 = 100.0
    
    result = dh(mass_enthalpy_1, mass_enthalpy_2)
    expected = -50.0
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


# === Tests for flow_coeff ===

def test_flow_coeff_man_definition():
    """Test flow coefficient with MAN definition."""
    Q = 10.0
    N = 3000
    D = 0.5
    
    result = flow_coeff(Q, N, D, DefType='MAN')
    
    assert not np.isnan(result), "MAN DefType should return valid result"
    assert isinstance(result, (float, np.floating)), "Result should be a float"


def test_flow_coeff_iso_definition():
    """Test flow coefficient with ISO 5389 definition."""
    Q = 10.0
    N = 3000
    D = 0.5
    
    result = flow_coeff(Q, N, D, DefType='ISO 5389')
    
    assert not np.isnan(result), "ISO 5389 DefType should return valid result"
    assert isinstance(result, (float, np.floating)), "Result should be a float"


def test_flow_coeff_different_definitions():
    """Test that different DefTypes give different results."""
    Q, N, D = 10.0, 3000, 0.5
    result_man = flow_coeff(Q, N, D, DefType='MAN')
    result_iso = flow_coeff(Q, N, D, DefType='ISO 5389')
    
    assert not np.isnan(result_man), "MAN DefType should return valid result"
    assert not np.isnan(result_iso), "ISO 5389 DefType should return valid result"
    assert result_man != result_iso, "Different DefTypes should give different results"


def test_flow_coeff_invalid_deftype():
    """Test that invalid DefType raises ValueError."""
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='INVALID')
    
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='invalid')
    
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='')


def test_flow_coeff_zero_speed():
    """Test scenarios leading to zero denominator return NaN."""
    # Zero speed results in zero denominator
    assert np.isnan(flow_coeff(10.0, 0, 0.5, DefType='MAN')), "Zero N"


# === Tests for impeller_tang_vel ===

def test_impeller_tang_vel():
    """Test impeller tangential velocity calculation."""
    N = 3000
    D = 0.5
    
    result = impeller_tang_vel(N, D)
    
    assert isinstance(result, (float, np.floating)), "Result should be a float"
    assert result > 0, "Tangential velocity should be positive for positive inputs"


def test_impeller_tang_vel_zero_speed():
    """Test with zero speed."""
    N = 0
    D = 0.5
    
    result = impeller_tang_vel(N, D)
    
    assert result == 0, "Zero speed should give zero velocity"


# === Tests for sigma_u_squared ===

def test_sigma_u_squared():
    """Test sigma U squared calculation from docstring example."""
    tipSpeedArray = np.array([3, 4, 5, 3, 4, 5])
    
    result = sigma_u_squared(tipSpeedArray)
    expected = 100
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_sigma_u_squared_different_array_sizes():
    """Test sigma_u_squared with various array sizes."""
    result1 = sigma_u_squared(np.array([3, 4, 5]))
    result2 = sigma_u_squared(np.array([3, 4, 5, 3, 4, 5]))
    
    assert result2 == 2 * result1, "Double array should give double result"


def test_sigma_u_squared_single_element():
    """Test with single element array."""
    result = sigma_u_squared(np.array([5]))
    expected = 25
    
    assert result == expected, f"Expected {expected}, got {result}"


# === Tests for poly_head_coeff ===

def test_poly_head_coeff():
    """Test polytropic head coefficient calculation from docstring example."""
    poly_head_val = 500
    sigma_u_squared_val = 900000
    
    result = poly_head_coeff(poly_head_val, sigma_u_squared_val)
    expected = 0.5555555555555556
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_poly_head_coeff_zero_sigma():
    """Test zero sigma_u_squared returns NaN."""
    assert np.isnan(poly_head_coeff(500, 0)), "Zero sigma_u_squared"


# === Tests for work_coefficient ===

def test_work_coefficient():
    """Test work coefficient calculation from docstring example."""
    dh_val = 1000
    sigma_u_squared_val = 2000000.0
    
    result = work_coefficient(dh_val, sigma_u_squared_val)
    expected = 0.5
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"


def test_work_coefficient_zero_sigma():
    """Test zero sigma_u_squared returns NaN."""
    assert np.isnan(work_coefficient(1000, 0)), "Zero sigma_u_squared"


# === Array Tests ===

def test_poly_exp_with_arrays():
    """Test poly_exp with numpy arrays."""
    p_suction = np.array([1.5, 2.0, 2.5])
    p_discharge = np.array([5.0, 6.0, 7.0])
    rho_suction = np.array([6.0, 7.0, 8.0])
    rho_discharge = np.array([12.0, 13.0, 14.0])
    
    result = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    
    assert isinstance(result, np.ndarray), "Result should be numpy array"
    assert len(result) == 3, "Result should have 3 elements"
    assert not np.any(np.isnan(result)), "No NaN values for valid inputs"


def test_poly_head_with_arrays():
    """Test poly_head with numpy arrays."""
    poly_exp_val = np.array([1.25, 1.30, 1.35])
    p_suction = np.array([1.0, 1.5, 2.0])
    p_discharge = np.array([5.0, 6.0, 7.0])
    rho_suction = np.array([10, 11, 12])
    rho_discharge = np.array([40, 42, 44])
    
    result = poly_head(poly_exp_val, p_suction, p_discharge, rho_suction, rho_discharge)
    
    assert isinstance(result, np.ndarray), "Result should be numpy array"
    assert len(result) == 3, "Result should have 3 elements"
    assert not np.any(np.isnan(result)), "No NaN values for valid inputs"


def test_flow_coeff_with_arrays():
    """Test flow_coeff with numpy arrays."""
    Q = np.array([10.0, 12.0, 14.0])
    N = np.array([3000, 3200, 3400])
    D = np.array([0.5, 0.52, 0.54])
    
    result = flow_coeff(Q, N, D, DefType='MAN')
    
    assert isinstance(result, np.ndarray), "Result should be numpy array"
    assert len(result) == 3, "Result should have 3 elements"
    assert not np.any(np.isnan(result)), "No NaN values for valid inputs"


# === Integration Tests ===

def test_compression_calculation_chain():
    """Test full compression calculation chain."""
    # Input conditions
    p_suction = 50.0
    p_discharge = 100.0
    rho_suction = 40.0
    rho_discharge = 75.0
    mass_enthalpy_1 = 500.0
    mass_enthalpy_2 = 600.0
    
    # Calculate chain
    n = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    assert not np.isnan(n), "Polytropic exponent should be valid"
    
    poly_head_val = poly_head(n, p_suction, p_discharge, rho_suction, rho_discharge)
    assert not np.isnan(poly_head_val), "Polytropic head should be valid"
    assert poly_head_val > 0, "Polytropic head should be positive"
    
    dh_val = dh(mass_enthalpy_1, mass_enthalpy_2)
    assert dh_val == 100.0, "Enthalpy rise should match"
    
    eff = poly_eff(poly_head_val, dh_val)
    assert not np.isnan(eff), "Efficiency should be valid"
    assert 0 < eff <= 1.0, "Efficiency should be between 0 and 1"
