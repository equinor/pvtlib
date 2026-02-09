# Compressor Function Migration Instructions

## Overview
This document outlines the migration of compressor-related functions from `equipment.py` to `compressors.py`.

**Key Migration Changes:**
- Convert static methods to standalone functions
- Rename to snake_case convention
- Update to NumPy docstring format
- **Implement comprehensive error handling** (two distinct patterns)
- Convert docstring examples to unit tests

## Migration Requirements

### Source
- **File**: `equipment.py`
- **Class**: `Compressor`
- **Current implementation**: Static methods within a class (`@staticmethod`)

### Destination
- **File**: `compressors.py`
- **New implementation**: Standalone functions (no class wrapper)

## Functions to Migrate

The following functions must be migrated from the `Compressor` class in `equipment.py`:

1. `compress_something(thing_to_compress)` - Example/placeholder function
2. `polyExp(p_suction, p_discharge, rho_suction, rho_discharge)` - Calculate polytropic exponent
3. `PolyHead(polyExp, p_suction, p_discharge, rho_suction, rho_discharge)` - Calculate polytropic head
4. `polyEff(PolyHead, dh)` - Calculate polytropic efficiency
5. `dh(mass_enthalpy_1, mass_enthalpy_2)` - Calculate specific mass enthalpy rise
6. `flow_coeff(Q, N, D, DefType='MAN')` - Calculate flow coefficient
7. `Impeller_tang_vel(N, D)` - Calculate impeller tangential velocity
8. `sigma_U_squared(tipSpeedArray)` - Calculate sigma U squared
9. `polyHeadCoeff(PolyHead, sigma_U_squared)` - Calculate polytropic head coefficient
10. `work_coefficient(dh, sigma_U_squared)` - Calculate work coefficient

## Naming Convention Changes

All function names must follow `snake_case` convention. The following functions require renaming:

| Old Name (equipment.py) | New Name (compressors.py) |
|-------------------------|---------------------------|
| `polyExp` | `poly_exp` |
| `PolyHead` | `poly_head` |
| `polyEff` | `poly_eff` |
| `Impeller_tang_vel` | `impeller_tang_vel` |
| `sigma_U_squared` | `sigma_u_squared` |
| `polyHeadCoeff` | `poly_head_coeff` |

Functions already in snake_case:
- `compress_something` ✓
- `flow_coeff` ✓
- `dh` ✓
- `work_coefficient` ✓

## Conversion Steps

### 1. Remove Class Wrapper
**Before (equipment.py):**
```python
class Compressor:
    @staticmethod
    def polyExp(p_suction, p_discharge, rho_suction, rho_discharge):
        # function body
        return polyExp
```

**After (compressors.py):**
```python
def poly_exp(p_suction, p_discharge, rho_suction, rho_discharge):
    # function body
    return poly_exp
```

### 2. Update Docstrings to NumPy Format

All docstrings must strictly follow NumPy docstring format:

```python
def poly_exp(p_suction, p_discharge, rho_suction, rho_discharge):
    """
    Calculate the polytropic exponent.

    Parameters
    ----------
    p_suction : float
        Suction pressure in bara.
    p_discharge : float
        Discharge pressure in bara.
    rho_suction : float
        Suction density in kg/m^3.
    rho_discharge : float
        Discharge density in kg/m^3.

    Returns
    -------
    float
        The polytropic exponent in [-].

    Examples
    --------
    >>> p_suction = 1.5
    >>> p_discharge = 5.0
    >>> rho_suction = 6.0
    >>> rho_discharge = 12.0
    >>> n = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    >>> print(n)
    1.7369655941662063
    """
```

**Key NumPy docstring requirements:**
- One-line summary followed by blank line
- Parameters section with type annotations
- Returns section with type and description
- Examples section with doctests where applicable
- Units specified in descriptions (e.g., "in bara", "in kg/m^3", "in [-]")

### 3. Update Variable Names
Internal variable names that match the old function name must be updated to match the new snake_case function name.

**Before:**
```python
def polyExp(...):
    polyExp = calculation
    return polyExp
```

**After:**
```python
def poly_exp(...):
    poly_exp = calculation
    return poly_exp
```

### 4. Update Example Code
All docstring examples must be updated to use the new function names:

**Before:**
```python
>>> result = Compressor.polyExp(1.5, 5.0, 6.0, 12.0)
```

**After:**
```python
>>> result = poly_exp(1.5, 5.0, 6.0, 12.0)
```

### 5. File Header
Add the standard MIT license header to `compressors.py` (copy from existing pvtlib files).

## Error Handling Pattern

### Critical: Two Distinct Error Handling Approaches

pvtlib uses **two different error handling strategies** depending on the type of error encountered. This is critical for the library's usability in large-scale data analysis.

### 1. Return `np.nan` for Real-World Invalid Measurements

**When to use:** Physical or measurement issues that can occur during normal operation.

**Purpose:** Prevents crashes during large-scale batch analysis where some data points may be invalid.

**Scenarios that should return `np.nan`:**
- **Division by zero** from physical measurements (zero pressure, zero density, zero velocity)
- **Negative values** for properties that must be positive (pressures, densities, temperatures in Kelvin)
- **Out-of-range physical values** (e.g., impossible compression ratios)
- **Invalid sensor readings** (e.g., measured value exceeds physical limits)
- **Non-physical conditions** (e.g., discharge pressure lower than suction pressure)
- **Undefined mathematical operations** on valid inputs (e.g., log of negative number from bad measurement)

**Code pattern:**
```python
def poly_exp(p_suction, p_discharge, rho_suction, rho_discharge):
    """Calculate the polytropic exponent."""
    
    # Check for invalid measurement values - return np.nan, don't raise exception
    if p_discharge == 0:
        return np.nan
    if rho_discharge == 0:
        return np.nan
    if p_suction == 0:
        return np.nan
    if rho_suction == 0:
        return np.nan
    
    # Perform calculation
    poly_exp = math.log(p_discharge / p_suction) / math.log(rho_discharge / rho_suction)
    
    return poly_exp
```

### 2. Raise Exceptions for Programming Errors

**When to use:** Incorrect function usage, wrong data types, or invalid configuration.

**Purpose:** Helps developers catch bugs during development and provides clear error messages.

**Scenarios that should raise exceptions:**
- **Wrong data types** (e.g., string passed instead of float)
- **Invalid units specification** (e.g., `units='invalid'` parameter)
- **Incorrect parameter combinations** (e.g., required parameter missing)
- **Invalid enum values** (e.g., `DefType='INVALID'` when only 'MAN' and 'ISO 5389' are valid)
- **Array dimension mismatches** (e.g., wrong shape for composition array)
- **Configuration errors** (e.g., AGA8 method name misspelled)

**Code pattern:**
```python
def flow_coeff(Q, N, D, DefType='MAN'):
    """Calculate the flow coefficient of a compressor."""
    
    # Validate DefType parameter - raise exception for programming error
    valid_types = ['MAN', 'ISO 5389']
    if DefType not in valid_types:
        raise ValueError(f"DefType must be one of {valid_types}, got '{DefType}'")
    
    # Calculate numerator based on definition type
    if DefType == 'MAN':
        numerator = Q
    elif DefType == 'ISO 5389':
        numerator = 4 * Q
    
    # Check for invalid measurement values - return np.nan
    U = D * np.pi * N / 60  # Tip speed
    
    if DefType == 'MAN':
        denominator = D**2 * U
    elif DefType == 'ISO 5389':
        denominator = np.pi * D**2 * U
    
    if denominator == 0:
        return np.nan
    
    flow_coeff = numerator / denominator
    return flow_coeff
```

### Error Handling Review for Each Function

Review and update error handling in each migrated function:

| Function | Current np.nan Returns | Potential ValueError Raises |
|----------|------------------------|----------------------------|
| `poly_exp` | Zero p_discharge, p_suction, rho_discharge, rho_suction | None needed |
| `poly_head` | Zero rho_discharge, rho_suction | None needed |
| `poly_eff` | Zero dh | None needed |
| `dh` | None (always valid) | None needed |
| `flow_coeff` | Zero denominator | Invalid DefType |
| `impeller_tang_vel` | None (check if needed) | None needed |
| `sigma_u_squared` | None (check if needed) | Invalid array type/shape? |
| `poly_head_coeff` | Zero sigma_u_squared | None needed |
| `work_coefficient` | Zero sigma_u_squared | None needed |

### Validation During Migration

For each function, verify:

1. **Identify all division operations** - add zero checks that return `np.nan`
2. **Check for parameter validation** - add `ValueError` for invalid options/enums
3. **Review physical constraints** - add checks for negative values of physical properties
4. **Consider edge cases** - what happens with extreme but valid values?
5. **Consistent checking order** - check programming errors (raise) before physical errors (return nan)

### Testing Error Handling

Both error types must be tested:

**Testing np.nan returns:**
```python
def test_poly_exp_zero_pressure():
    """Test that invalid pressure measurements return NaN."""
    result = poly_exp(0, 5.0, 6.0, 12.0)
    assert np.isnan(result), "Expected NaN for zero suction pressure"

def test_poly_exp_zero_density():
    """Test that invalid density measurements return NaN."""
    result = poly_exp(1.5, 5.0, 0, 12.0)
    assert np.isnan(result), "Expected NaN for zero suction density"
```

**Testing exception raises:**
```python
def test_flow_coeff_invalid_deftype():
    """Test that invalid DefType raises ValueError."""
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='INVALID')

def test_flow_coeff_valid_deftypes():
    """Test that valid DefTypes work correctly."""
    result_man = flow_coeff(10.0, 3000, 0.5, DefType='MAN')
    result_iso = flow_coeff(10.0, 3000, 0.5, DefType='ISO 5389')
    assert not np.isnan(result_man), "MAN DefType should work"
    assert not np.isnan(result_iso), "ISO 5389 DefType should work"
```

### Documentation in Docstrings

Document error behavior in function docstrings:

```python
def poly_exp(p_suction, p_discharge, rho_suction, rho_discharge):
    """
    Calculate the polytropic exponent.

    Parameters
    ----------
    p_suction : float
        Suction pressure in bara. Must be positive.
    p_discharge : float
        Discharge pressure in bara. Must be positive.
    rho_suction : float
        Suction density in kg/m^3. Must be positive.
    rho_discharge : float
        Discharge density in kg/m^3. Must be positive.

    Returns
    -------
    float
        The polytropic exponent in [-], or np.nan if any input is zero
        or the calculation results in invalid values.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero pressures or densities)
    to prevent crashes during batch processing of measurement data.

    Examples
    --------
    >>> p_suction = 1.5
    >>> p_discharge = 5.0
    >>> rho_suction = 6.0
    >>> rho_discharge = 12.0
    >>> n = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    >>> print(n)
    1.7369655941662063
    
    Invalid measurements return NaN:
    >>> poly_exp(0, 5.0, 6.0, 12.0)
    nan
    """
```

### Quick Reference: Error Handling Decision Tree

```
Is the error from:
├─ Invalid measurement/sensor data? → Return np.nan
│  ├─ Zero pressure, density, or flow
│  ├─ Negative physical properties
│  ├─ Out-of-range sensor readings
│  └─ Non-physical measurement combinations
│
└─ Incorrect function usage? → Raise ValueError
   ├─ Invalid parameter options (e.g., wrong DefType)
   ├─ Wrong data types
   ├─ Missing required parameters
   └─ Invalid configuration
```

## Required Imports

Add necessary imports to `compressors.py`:
```python
import numpy as np
```

**Note:** Use `numpy` functions (e.g., `np.log`) instead of `math` module functions to support both scalar values and numpy arrays.

## Testing Requirements

### Overview
All functions in `equipment.py` contain docstring examples. These examples must be converted to unit tests in `tests/test_compressors.py`.

### Test File Structure
Create `tests/test_compressors.py` following the standard pvtlib test pattern:
```python
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
from pvtlib.equipment.compressors import poly_exp, poly_head, poly_eff, dh, flow_coeff, impeller_tang_vel, sigma_u_squared, poly_head_coeff, work_coefficient

# Test functions here
```

### Converting Docstring Examples to Tests

Each function with examples in its docstring must have corresponding unit tests. Extract the example values and expected results to create test functions.

**Example - Converting `poly_exp` docstring example:**

**Docstring example:**
```python
Examples
--------
>>> p_suction = 1.5
>>> p_discharge = 5.0
>>> rho_suction = 6.0
>>> rho_discharge = 12.0
>>> n = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
>>> print(n)
1.7369655941662063
```

**Corresponding unit test:**
```python
def test_poly_exp():
    """Test polytropic exponent calculation from docstring example."""
    p_suction = 1.5
    p_discharge = 5.0
    rho_suction = 6.0
    rho_discharge = 12.0
    
    result = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    expected = 1.7369655941662063
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"

def test_poly_exp_zero_discharge_pressure():
    """Test that poly_exp returns NaN when discharge pressure is zero."""
    result = poly_exp(1.5, 0, 6.0, 12.0)
    assert np.isnan(result), "Expected NaN for zero discharge pressure"

def test_poly_exp_zero_density():
    """Test that poly_exp returns NaN for zero density values."""
    result1 = poly_exp(1.5, 5.0, 0, 12.0)
    result2 = poly_exp(1.5, 5.0, 6.0, 0)
    assert np.isnan(result1), "Expected NaN for zero suction density"
    assert np.isnan(result2), "Expected NaN for zero discharge density"
```

**Example - Converting `poly_head` docstring example:**

**Docstring example:**
```python
Examples
--------
>>> polyExp = 1.25
>>> p_suction = 1.0
>>> p_discharge = 5.0
>>> rho_suction = 10
>>> rho_discharge = 40
>>> result = Compressor.PolyHead(polyExp, p_suction, p_discharge, rho_suction, rho_discharge)
>>> print(result)
480.0
```

**Corresponding unit test:**
```python
def test_poly_head():
    """Test polytropic head calculation from docstring example."""
    poly_exp_val = 1.25
    p_suction = 1.0
    p_discharge = 5.0
    rho_suction = 10
    rho_discharge = 40
    
    result = poly_head(poly_exp_val, p_suction, p_discharge, rho_suction, rho_discharge)
    expected = 480.0
    
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"
```

### Test Requirements

1. **Create `tests/test_compressors.py`** with MIT license header
2. **One test function per compressor function** minimum
3. **Use docstring examples as test cases** - extract input values and expected outputs
4. **Test function naming**: `test_<function_name>()` (e.g., `test_poly_exp()`, `test_poly_head()`)
5. **Add edge case tests** for error handling (zero divisions, invalid inputs that should return `np.nan`)
6. **Use appropriate assertions**:
   - `np.isclose(result, expected)` for floating-point comparisons
   - `np.isnan(result)` for expected NaN returns
7. **Include docstrings in test functions** describing what is being tested
8. **Update any existing tests** in `tests/` that reference `Compressor` class

### Functions with Existing Docstring Examples

The following functions have examples that should be converted to tests:

| Function (new name) | Has Example | Test Priority |
|---------------------|-------------|---------------|
| `compress_something` | ✓ | Low (placeholder function) |
| `poly_exp` | ✓ | High |
| `poly_head` | ✓ | High |
| `poly_eff` | ✓ | High |
| `dh` | ✓ | High |
| `flow_coeff` | ? | High (check docstring) |
| `impeller_tang_vel` | ? | Medium |
| `sigma_u_squared` | ✓ | High |
| `poly_head_coeff` | ✓ | High |
| `work_coefficient` | ✓ | High |

### Additional Test Cases to Add

Beyond docstring examples, add comprehensive tests for error handling and array support:

#### 0. Test Array Support

**Required for all functions to ensure numpy array compatibility:**

```python
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

def test_poly_exp_with_mixed_valid_invalid_arrays():
    """Test poly_exp with arrays containing some zero values."""
    p_suction = np.array([1.5, 0, 2.5])
    p_discharge = np.array([5.0, 6.0, 7.0])
    rho_suction = np.array([6.0, 7.0, 8.0])
    rho_discharge = np.array([12.0, 13.0, 14.0])
    
    result = poly_exp(p_suction, p_discharge, rho_suction, rho_discharge)
    
    assert isinstance(result, np.ndarray), "Result should be numpy array"
    assert np.isnan(result[1]), "Second element should be NaN due to zero p_suction"
    assert not np.isnan(result[0]), "First element should be valid"
    assert not np.isnan(result[2]), "Third element should be valid"

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
```

#### 1. Test `np.nan` Returns (Real-World Invalid Measurements)

**Required for each function with division or physical constraints:**

```python
def test_poly_exp_all_zero_cases():
    """Test all zero-value scenarios return NaN."""
    assert np.isnan(poly_exp(0, 5.0, 6.0, 12.0)), "Zero p_suction"
    assert np.isnan(poly_exp(1.5, 0, 6.0, 12.0)), "Zero p_discharge"
    assert np.isnan(poly_exp(1.5, 5.0, 0, 12.0)), "Zero rho_suction"
    assert np.isnan(poly_exp(1.5, 5.0, 6.0, 0)), "Zero rho_discharge"

def test_poly_head_zero_density():
    """Test zero density values return NaN."""
    assert np.isnan(poly_head(1.25, 1.0, 5.0, 0, 40)), "Zero rho_suction"
    assert np.isnan(poly_head(1.25, 1.0, 5.0, 10, 0)), "Zero rho_discharge"

def test_poly_eff_zero_dh():
    """Test zero enthalpy rise returns NaN."""
    assert np.isnan(poly_eff(80.0, 0)), "Zero dh"

def test_flow_coeff_zero_denominator():
    """Test scenarios leading to zero denominator return NaN."""
    # Zero speed results in zero denominator
    assert np.isnan(flow_coeff(10.0, 0, 0.5, DefType='MAN')), "Zero N"

def test_poly_head_coeff_zero_sigma():
    """Test zero sigma_u_squared returns NaN."""
    assert np.isnan(poly_head_coeff(500, 0)), "Zero sigma_u_squared"

def test_work_coefficient_zero_sigma():
    """Test zero sigma_u_squared returns NaN."""
    assert np.isnan(work_coefficient(1000, 0)), "Zero sigma_u_squared"
```

#### 2. Test Exception Raises (Programming Errors)

**Required for functions with parameter validation:**

```python
def test_flow_coeff_invalid_deftype():
    """Test that invalid DefType raises ValueError."""
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='INVALID')
    
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='invalid')
    
    with pytest.raises(ValueError, match="DefType must be one of"):
        flow_coeff(10.0, 3000, 0.5, DefType='')

def test_flow_coeff_valid_deftypes():
    """Test both valid DefType values work correctly."""
    Q, N, D = 10.0, 3000, 0.5
    result_man = flow_coeff(Q, N, D, DefType='MAN')
    result_iso = flow_coeff(Q, N, D, DefType='ISO 5389')
    
    assert not np.isnan(result_man), "MAN DefType should return valid result"
    assert not np.isnan(result_iso), "ISO 5389 DefType should return valid result"
    assert result_man != result_iso, "Different DefTypes should give different results"

# Add type checking tests if applicable
def test_sigma_u_squared_invalid_input():
    """Test that invalid array input raises appropriate error."""
    # Determine if this should raise ValueError or return NaN based on implementation
    pass  # Implement after reviewing function requirements
```

#### 3. Edge Cases and Boundary Testing

```python
def test_poly_exp_equal_pressures():
    """Test behavior when suction and discharge pressures are equal."""
    # log(1) = 0, could cause issues
    result = poly_exp(5.0, 5.0, 6.0, 12.0)
    # Verify expected behavior (likely returns 0 or NaN)
    
def test_poly_exp_very_small_values():
    """Test with very small but non-zero values."""
    result = poly_exp(1e-6, 1e-5, 1e-6, 1e-5)
    assert not np.isnan(result), "Small valid values should not return NaN"

def test_poly_exp_very_large_values():
    """Test with very large values."""
    result = poly_exp(1e6, 1e7, 1e6, 1e7)
    assert not np.isnan(result), "Large valid values should not return NaN"

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
```

#### 4. Physical Realism Tests (Optional but Recommended)

```python
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

def test_poly_eff_physical_limits():
    """Test that efficiency is between 0 and 1."""
    poly_head_val = 80.0
    dh_val = 100.0
    
    result = poly_eff(poly_head_val, dh_val)
    
    # Polytropic efficiency should be between 0 and 1
    assert 0 < result <= 1.0, f"Unrealistic efficiency: {result}"
```

#### 5. Integration Tests (Function Chains)

```python
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
```

#### Test Organization

Organize tests logically in `test_compressors.py`:

```python
# === Tests for poly_exp ===
def test_poly_exp():
    """Test basic calculation from docstring example."""
    pass

def test_poly_exp_all_zero_cases():
    """Test error handling for zero inputs."""
    pass

def test_poly_exp_realistic_values():
    """Test with realistic compression values."""
    pass

# === Tests for poly_head ===
def test_poly_head():
    """Test basic calculation from docstring example."""
    pass

def test_poly_head_zero_density():
    """Test error handling for zero density."""
    pass

# ... and so on for each function
```

### Running Tests

After creating tests:
```bash
pytest tests/test_compressors.py -v
```

Or run all tests:
```bash
pytest tests/ -v
```

### Test Coverage

Ensure all functions are tested:
```bash
pytest tests/test_compressors.py --cov=pvtlib.equipment.compressors --cov-report=html
```

## Documentation Updates

After migration, update:
1. `pvtlib/equipment/__init__.py` - Add module import: `from . import compressors`
2. `README.md` - Update any references to compressor functionality
3. Function return dictionaries should have descriptive keys (follow pvtlib pattern)

**Note:** Following pvtlib convention, the `__init__.py` imports the module, not individual functions:
```python
from . import compressors
from . import separators
from . import valves
```

Users import functions directly from the module:
```python
from pvtlib.equipment.compressors import poly_exp, poly_head
```

## Deprecation Notice

Once migration is complete, `equipment.py` should either:
- Be deprecated with a clear notice pointing to `compressors.py`
- Have the `Compressor` class removed entirely
- Keep only non-compressor functionality (if any exists)

## Validation Checklist

Before considering migration complete:

### Code Migration
- [ ] All functions migrated from `Compressor` class to `compressors.py`
- [ ] All function names converted to snake_case
- [ ] All docstrings in NumPy format
- [ ] Internal variable names updated to match new function names
- [ ] All docstring example code updated (no `Compressor.methodName()` references)
- [ ] MIT license header added to `compressors.py`
- [ ] Required imports added (`numpy` only - supports both scalars and arrays)

### Error Handling
- [ ] All division operations checked for zero denominators (return `np.nan`)
- [ ] All parameter validations added (raise `ValueError` for invalid enum/options)
- [ ] Physical constraints validated (negative pressures/densities checked)
- [ ] Consistent error checking order (programming errors first, then measurement errors)
- [ ] Error behavior documented in docstrings (Notes section)
- [ ] Invalid measurement examples added to docstrings
- [ ] `flow_coeff` validates DefType parameter (raises `ValueError` for invalid)

### Testing
- [ ] `tests/test_compressors.py` created with MIT license header
- [ ] All docstring examples converted to unit tests
- [ ] One test function per compressor function (minimum)
- [ ] **Array support tests** added for all functions (test with numpy arrays)
- [ ] **np.nan return tests** added for all zero-value scenarios
- [ ] **ValueError tests** added for invalid parameter values
- [ ] Edge case tests added (equal pressures, very small/large values)
- [ ] Both DefType values tested in `flow_coeff` ('MAN' and 'ISO 5389')
- [ ] Invalid DefType test added for `flow_coeff`
- [ ] Physical realism tests added (optional but recommended)
- [ ] Integration/chain tests added (optional but recommended)
- [ ] All tests passing (`pytest tests/test_compressors.py -v`)
- [ ] No references to old `Compressor` class in test suite
- [ ] Test coverage verified (optional but recommended)

### Integration
- [ ] Module import added to `pvtlib/equipment/__init__.py` (`from . import compressors`)
- [ ] Usage in examples folder updated (if any)
- [ ] No usage of old `Compressor` class in codebase
- [ ] `equipment.py` updated (deprecated/removed `Compressor` class)

### Documentation
- [ ] `README.md` updated if it references compressor functionality
- [ ] All function return types verified (use dictionaries with descriptive keys if multiple returns)
- [ ] Error handling behavior clearly documented
