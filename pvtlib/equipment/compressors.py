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
        The polytropic exponent in [-], or np.nan if any input is zero.

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
    # Convert to arrays for consistent handling
    p_suction = np.asarray(p_suction, dtype=float)
    p_discharge = np.asarray(p_discharge, dtype=float)
    rho_suction = np.asarray(rho_suction, dtype=float)
    rho_discharge = np.asarray(rho_discharge, dtype=float)
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.log(p_discharge / p_suction) / np.log(rho_discharge / rho_suction)
    
    # Set NaN where inputs are zero
    mask = (p_discharge == 0) | (rho_discharge == 0) | (p_suction == 0) | (rho_suction == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result


def poly_head(n, p_suction, p_discharge, rho_suction, rho_discharge):
    """
    Calculate the polytropic head of a compressor.

    Parameters
    ----------
    n : float
        The polytropic exponent of the compressor in [-]. Must be positive.
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
        The polytropic head in kJ/kg, or np.nan if density values are zero.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero densities) to prevent
    crashes during batch processing of measurement data.

    Examples
    --------
    Calculate the polytropic head for given parameters:

    >>> n = 1.25
    >>> p_suction = 1.0
    >>> p_discharge = 5.0
    >>> rho_suction = 10
    >>> rho_discharge = 40
    >>> result = poly_head(n, p_suction, p_discharge, rho_suction, rho_discharge)
    >>> print(result)
    480.0
    
    Invalid measurements return NaN:
    
    >>> poly_head(1.25, 1.0, 5.0, 0, 40)
    nan
    """
    # Convert to arrays for consistent handling
    n = np.asarray(n, dtype=float)
    p_suction = np.asarray(p_suction, dtype=float)
    p_discharge = np.asarray(p_discharge, dtype=float)
    rho_suction = np.asarray(rho_suction, dtype=float)
    rho_discharge = np.asarray(rho_discharge, dtype=float)
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = 100 * (n / (n - 1)) * (
                    (p_discharge / rho_discharge) - (p_suction / rho_suction))
    
    # Set NaN where densities are zero
    mask = (rho_discharge == 0) | (rho_suction == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result


def poly_eff(head, enthalpy_rise):
    """
    Calculate the polytropic efficiency of the stage.

    Parameters
    ----------
    head : float
        The polytropic head of the stage in kJ/kg. Must be positive.
    enthalpy_rise : float
        The specific mass enthalpy rise over the stage in kJ/kg. Must be non-zero.

    Returns
    -------
    float
        The polytropic efficiency in [-], or np.nan if enthalpy_rise is zero.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero enthalpy rise) to prevent
    crashes during batch processing of measurement data.

    Examples
    --------
    Calculate the polytropic efficiency for given parameters:

    >>> head = 80.0
    >>> enthalpy_rise = 100.0
    >>> result = poly_eff(head, enthalpy_rise)
    >>> print(result)
    0.8
    
    Invalid measurements return NaN:
    
    >>> poly_eff(80.0, 0)
    nan
    """
    # Convert to arrays for consistent handling
    head = np.asarray(head, dtype=float)
    enthalpy_rise = np.asarray(enthalpy_rise, dtype=float)
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = head / enthalpy_rise
    
    # Set NaN where enthalpy_rise is zero
    mask = (enthalpy_rise == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result


def dh(mass_enthalpy_1, mass_enthalpy_2):
    """
    Calculate the specific mass enthalpy rise of the compressor.

    Parameters
    ----------
    mass_enthalpy_1 : float
        The inlet specific mass enthalpy in kJ/kg.
    mass_enthalpy_2 : float
        The discharge specific mass enthalpy in kJ/kg.

    Returns
    -------
    float
        The specific mass enthalpy rise in kJ/kg.

    Examples
    --------
    Calculate the specific mass enthalpy rise for given parameters:

    >>> mass_enthalpy_1 = 100.0
    >>> mass_enthalpy_2 = 150.0
    >>> result = dh(mass_enthalpy_1, mass_enthalpy_2)
    >>> print(result)
    50.0
    """
    dh = mass_enthalpy_2 - mass_enthalpy_1
    
    return dh


def flow_coeff(Q, N, D, DefType='MAN'):
    """
    Calculate the flow coefficient of a compressor.

    Parameters
    ----------
    Q : float
        Fluid volumetric flow at compressor inlet in m^3/s.
    N : float
        Compressor speed in rpm.
    D : float
        First impeller diameter in m.
    DefType : str, optional
        Definition type for flow coefficient calculation. Must be either 'MAN' 
        or 'ISO 5389'. Default is 'MAN'.

    Returns
    -------
    float
        Flow coefficient in [-], or np.nan if denominator is zero.

    Raises
    ------
    ValueError
        If DefType is not 'MAN' or 'ISO 5389'.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero denominator) to prevent
    crashes during batch processing of measurement data.
    
    The function supports two definition types:
    - 'MAN': Manufacturer's definition
    - 'ISO 5389': ISO standard definition

    Examples
    --------
    Calculate flow coefficient using manufacturer's definition:

    >>> Q = 10.0
    >>> N = 3000
    >>> D = 0.5
    >>> result = flow_coeff(Q, N, D, DefType='MAN')
    >>> isinstance(result, float)
    True
    
    Invalid DefType raises ValueError:
    
    >>> flow_coeff(10.0, 3000, 0.5, DefType='INVALID')  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    ValueError: DefType must be one of ['MAN', 'ISO 5389'], got 'INVALID'
    """
    # Validate DefType parameter - raise exception for programming error
    valid_types = ['MAN', 'ISO 5389']
    if DefType not in valid_types:
        raise ValueError(f"DefType must be one of {valid_types}, got '{DefType}'")
    
    # Calculate numerator based on definition type
    if DefType == 'MAN':
        numerator = Q
    elif DefType == 'ISO 5389':
        numerator = 4 * Q
    
    # Convert to arrays for consistent handling
    Q = np.asarray(Q, dtype=float)
    N = np.asarray(N, dtype=float)
    D = np.asarray(D, dtype=float)
    
    # Calculate denominator
    U = D * np.pi * N / 60  # Tip speed
    
    if DefType == 'MAN':
        denominator = D**2 * U
    elif DefType == 'ISO 5389':
        denominator = np.pi * D**2 * U
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = numerator / denominator
    
    # Set NaN where denominator is zero
    mask = (denominator == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result


def impeller_tang_vel(N, D):
    """
    Calculate impeller tangential velocity.

    Parameters
    ----------
    N : float
        Compressor speed in rpm.
    D : float
        Impeller outer diameter in m.

    Returns
    -------
    float
        Impeller tangential velocity in m/s.

    Examples
    --------
    Calculate impeller tangential velocity:

    >>> N = 3000
    >>> D = 0.5
    >>> result = impeller_tang_vel(N, D)
    >>> isinstance(result, float)
    True
    """
    impeller_tang_vel = 2 * np.pi * N * D / (2 * 60)
    
    return impeller_tang_vel


def sigma_u_squared(tipSpeedArray):
    """
    Calculate the sigma U squared of the compressor.

    Parameters
    ----------
    tipSpeedArray : numpy.ndarray or float
        Tip speeds in m/s.

    Returns
    -------
    float
        The sigma U squared in m^2/s^2 (J/kg).

    Notes
    -----
    This function calculates the sum of squared tip speeds, which is used in
    compressor performance calculations.

    Examples
    --------
    Calculate the sigma U squared for given parameters:

    >>> import numpy as np
    >>> tipSpeedArray = np.array([3, 4, 5, 3, 4, 5])
    >>> result = sigma_u_squared(tipSpeedArray)
    >>> print(result)
    100
    """
    sigma_u_squared = np.sum(tipSpeedArray ** 2)
    
    return sigma_u_squared


def poly_head_coeff(head, sigma_u_sq):
    """
    Calculate the polytropic head coefficient of the compressor.

    Parameters
    ----------
    head : float
        The polytropic head of the compressor in kJ/kg.
    sigma_u_sq : float
        Sigma U^2 in J/kg (m^2/s^2). Must be non-zero.

    Returns
    -------
    float
        The polytropic head coefficient in [-], or np.nan if sigma_u_sq is zero.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero sigma_u_sq) to prevent
    crashes during batch processing of measurement data.
    
    This function calculates the polytropic head coefficient using the provided parameters.

    Examples
    --------
    Calculate the polytropic head coefficient for given parameters:

    >>> head = 500
    >>> sigma_u_sq = 900000
    >>> result = poly_head_coeff(head, sigma_u_sq)
    >>> print(result)
    0.5555555555555556
    
    Invalid measurements return NaN:
    
    >>> poly_head_coeff(500, 0)
    nan
    """
    # Convert to arrays for consistent handling
    head = np.asarray(head, dtype=float)
    sigma_u_sq = np.asarray(sigma_u_sq, dtype=float)
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = (1000 * head) / sigma_u_sq
    
    # Set NaN where sigma_u_sq is zero
    mask = (sigma_u_sq == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result


def work_coefficient(enthalpy_rise, sigma_u_sq):
    """
    Calculate the work coefficient of the compressor.

    Parameters
    ----------
    enthalpy_rise : float
        The specific mass enthalpy rise of the compressor in kJ/kg.
    sigma_u_sq : float
        Sigma U^2 in J/kg (m^2/s^2). Must be non-zero.

    Returns
    -------
    float
        The work coefficient of the compressor in [-], or np.nan if sigma_u_sq is zero.

    Notes
    -----
    Returns np.nan for invalid measurement values (zero sigma_u_sq) to prevent
    crashes during batch processing of measurement data.
    
    This function calculates the work coefficient using the provided parameters.

    Examples
    --------
    Calculate the work coefficient for given parameters:

    >>> enthalpy_rise = 1000
    >>> sigma_u_sq = 2000000.0
    >>> result = work_coefficient(enthalpy_rise, sigma_u_sq)
    >>> print(result)
    0.5
    
    Invalid measurements return NaN:
    
    >>> work_coefficient(1000, 0)
    nan
    """
    # Convert to arrays for consistent handling
    enthalpy_rise = np.asarray(enthalpy_rise, dtype=float)
    sigma_u_sq = np.asarray(sigma_u_sq, dtype=float)
    
    # Calculate with numpy (handles arrays)
    with np.errstate(divide='ignore', invalid='ignore'):
        result = (1000 * enthalpy_rise) / sigma_u_sq
    
    # Set NaN where sigma_u_sq is zero
    mask = (sigma_u_sq == 0)
    result = np.where(mask, np.nan, result)
    
    # Return scalar if input was scalar
    return result.item() if result.ndim == 0 else result
