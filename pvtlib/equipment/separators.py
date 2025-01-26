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
import numpy as np

def scrubber_K_value(Usg, rho_gas, rho_liquid):
    '''
    Scrubber K-value

    Parameters
    ----------
    Usg : float
        Superficial gas velocity [m/s]
    rho_gas : float
        Gas density [kg/m3]
    rho_liquid : float
        Liquid density (oil, water or total liquid) [kg/m3]

    Returns
    -------
    K_value : float
        Scrubber K_value [m/s]
    '''
    
    if rho_liquid-rho_gas <= 0: #Check that gas density is smaller than liquid density to prevent divide by zero or square root of negative
        K_value = np.nan
    elif (rho_gas<0): #Check that gas density is a positive number to prevent square root of negative
        K_value = np.nan
    else:
        K_value = Usg*math.sqrt(rho_gas/(rho_liquid-rho_gas))
    return K_value


def scrubber_inlet_momentum(u, rho):
    '''
    Calculates the inlet momentum of a scrubber given the velocity and density of the fluid.
    For inlet momentum of a fluid mixture (gas and liquid), use mixture density and mixture velocity

    Parameters
    ----------
    u : float
        Velocity of the fluid [m/s].
    rho : float
        Density of the fluid [kg/m^3].

    Returns
    -------
    float
        Inlet momentum of the scrubber [Pa].

    '''
    
    return rho*u**2