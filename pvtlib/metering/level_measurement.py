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

def level_from_differential_pressure(dP, rho1, rho2, h, g=9.80665, check_input=False):
    """
    Calculate level from differential pressure measurement. 
    The calculation assumes that the fluid with density rho1 is above the fluid with density rho2
    and that the differential pressure measurement is positive, 
    meaning that the pressure at the lower tapping is higher than at the upper tapping for static fluids. 
    The differential pressure is measured between the top tapping and bottom tapping. Level is measured above the bottom tapping. 

    Parameters
    ----------
    dP : float
        Differential pressure [mbar].
    rho1 : float
        Density of fluid 1 [kg/m³].
    rho2 : float
        Density of fluid 2 [kg/m³].
    h : float
        Total height of the differential pressure sensor [m].
    g : float, optional
        Acceleration due to gravity. The default is 9.80665 [m/s²]. 
    check_input : bool, optional
        If True, raise an error if the input is invalid. The default is False, in which case np.nan is returned.

    Returns
    -------
    h2 : float
        Level of fluid 2 above bottom tapping [m].
    """

    # Check that dP is positive
    if dP < 0:
        if check_input:
            raise ValueError("dP must be positive")
        else:
            return np.nan
        
    # Check that h is positive
    if h < 0:
        if check_input:
            raise ValueError("h must be positive")
        else:
            return np.nan

    dP_Pa = dP * 100 # Convert to Pa

    # Check if rho1 is less than rho2
    if rho1 >= rho2:
        if check_input:
            raise ValueError("rho1 must be less than rho2")
        else:
            return np.nan

    h2 = (dP_Pa - rho1 * g * h) / (g * (rho2 - rho1))

    return h2

def static_fluid_pressure(rho, h, pressure_unit='mbar', g=9.80665):
    """
    Calculate the static pressure of a fluid column of height h and density rho. 

    Parameters
    ----------
    rho : float
        Density of the fluid [kg/m³].
    h : float
        Height of the fluid column [m].
    pressure_unit : str, optional
        Unit of the pressure. The default is 'mbar'.
    g : float, optional
        Acceleration due to gravity. The default is 9.80665 [m/s²].

    Returns
    -------
    p : float
        Static pressure [mbar].
    """
    p_Pa = rho * g * h
    if pressure_unit.lower() == 'pa':
        p = p_Pa
    elif pressure_unit.lower() == 'mbar':
        p = p_Pa / 100
    elif pressure_unit.lower() in ['bar', 'bara']:
        p = p_Pa / 100000
    else:
        raise ValueError("pressure_unit must be 'pa', 'mbar', 'bar' or 'bara'")

    return p