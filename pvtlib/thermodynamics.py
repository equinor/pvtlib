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

from pvtlib import unit_converters
import math

def energy_rate_balance(h_in, h_out, massflow, vel_in, vel_out):
    '''
    Energy rate balance over control volume

    Parameters
    ----------
    h_in : float
        Enthalpy in [kJ/kg]
    h_out : float
        Enthalpy out [kJ/kg]
    massflow : float
        Mass flow [kg/s]
    vel_in : float
        Velocity in [m/s]
    vel_out : float
        Velocity out [m/s]

    Returns
    -------
    energy_rate_change : float
        Energy rate change [kW]

    '''
    
    energy_rate_in = massflow*(h_in*1000 + ((vel_in**2)/2))/1000
    energy_rate_out = massflow*(h_out*1000 + ((vel_out**2)/2))/1000
        
    energy_rate_change = energy_rate_in - energy_rate_out
    
    return energy_rate_change
                            

def energy_rate_difference(energy_rate_A, energy_rate_B):
    '''
    Difference in energy rate between A and B, absolute values
    
    Parameters
    ----------
    energy_rate_A : float
        Energy rate A [kW]
    energy_rate_B : float
        Energy rate B [kW]

    Returns
    -------
    energy_rate_difference : float
        Difference between energy rate A and B [kW]

    '''
    
    energy_rate_difference = abs(energy_rate_A) - abs(energy_rate_B)
    
    return energy_rate_difference

def energy_rate_diffperc(energy_rate_A, energy_rate_B):
    '''
    Diff percent in energy rate between A and B, absolute values

    Parameters
    ----------
    energy_rate_A : float
        Energy rate A [kW]
    energy_rate_B : float
        Energy rate B [kW]

    Returns
    -------
    energy_rate_diffperc : float
        Difference percentage between energy rate A and B [%]

    '''
    
    energy_rate_diffperc = 100*(abs(energy_rate_A) - abs(energy_rate_B))/((abs(energy_rate_A) + abs(energy_rate_B))/2)
    
    return energy_rate_diffperc


def natural_gas_viscosity_Lee_et_al(T, M, rho):
    '''
    Calculate natural gas viscosity using Lee et al. correlation. 
    Correlation developed for natural gases at pressures between 100 psia (6.9 bar) and 8000 psia (551 bar) and temperatures between 100 and 340 F (37.8 and 171.1 C)

    Parameters
    ----------
    T : float
        Temperature [C]
    M : float
        Molar mass [g/mol]
    rho : float
        Density [kg/m3]

    Returns
    -------
    mu : float
        Viscosity [cP]

    Notes
    -----
    The correlation is developed for hydrocarbon natural gases at certain condistions and may not be valid for other gases.
    However, the simplicity of the correlation makes it a good choice for quick calculations where high accuracy is not required.

    Lee, A.L., M.H. Gonzalez, and B.E. Eakin, The Viscosity of Natural Gases. Journal of Petroleum Technology, 1966 
    https://petrowiki.spe.org/Gas_viscosity
    '''

    T_R = unit_converters.celsius_to_rankine(T)
    rho_gpercm3 = rho/1000

    K1 = ((9.4+0.02*M)*T_R**1.5)/(209+19*M+T_R)
    X = 3.5+(986/T_R)+0.01*M
    Y = 2.4-0.2*X

    mu = K1*math.exp(X*(rho_gpercm3)**Y)/1e4 #Convert from microPoise to cP

    return mu
