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

    T_R = (T + 273.15) * 9/5  # Convert Celsius to Rankine
    rho_gpercm3 = rho/1000

    K1 = ((9.4+0.02*M)*T_R**1.5)/(209+19*M+T_R)
    X = 3.5+(986/T_R)+0.01*M
    Y = 2.4-0.2*X

    mu = K1*math.exp(X*(rho_gpercm3)**Y)/1e4 #Convert from microPoise to cP

    return mu

#%% Speed of sound based methods for determining physical properties
def density_from_sos_kappa(measured_sos, kappa, pressure_bara):
    '''
    Calculate gas density from speed of sound, isentropic exponent and pressure.
    The method is described in [1]_ from the GFMW2024. 

    Parameters
    ----------
    measured_sos : float
        Measured Speed of Sound [m/s]
        Measured Speed of Sound [m/s]
    kappa : float
        Isentropic Exponent calculated by appropriate equation of state [-]
    pressure_bara : float
        Measured pressure [bara]

    Returns
    -------
    rho : float
        Gas density from speed of sound, isentropic exponent and pressure [kg/m3]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    
    P_Pa = pressure_bara*10**5
    
    if measured_sos==0:
        rho = np.nan
    else:
        rho = kappa * P_Pa/(measured_sos**2)

    return rho

def sos_from_rho_kappa(measured_rho, kappa, pressure_bara):
    '''
    Calculate speed of sound from density, isentropic exponent and pressure. 
    The method is described in [1]_ from the GFMW2024. 

    Parameters
    ----------
    measured_rho : float
        Measured gas density [kg/m3]
    kappa : float
        Isentropic Exponent calculated by appropriate equation of state [-]
    pressure_bara : float
        Measured pressure [bara]

    Returns
    -------
    sos : float
        Speed of sound [m/s]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    P_Pa = pressure_bara * 1e5

    denominator = measured_rho
    numerator = kappa * P_Pa

    if denominator == 0 or numerator / denominator < 0:
        sos = np.nan
    else:
        sos = np.sqrt(numerator / denominator)

    return sos

def molar_mass_from_sos_kappa(measured_sos, kappa, Z, temperature_C, R=8.3144621):
    '''
    Calculate molar mass from measured speed of sound, isentropic exponent, compressibility factor, and temperature.
    Based on the principles described in [1]_ from GFMW2024. 

    Same equation of state must be used to establish both kappa and Z, otherwise it can cause inconsistencies.

    Parameters
    ----------
    measured_sos : float
        Measured speed of sound [m/s]
    kappa : float
        Isentropic exponent calculated by appropriate equation of state [-]
    Z : float
        Compressibility factor calculated by appropriate equation of state [-]
    temperature_C : float
        Temperature [C]
    R : float, optional
        Universal gas constant [J/(mol·K)]. Default is 8.3144621 (GERG-2008).

    Returns
    -------
    M : float
        Molar mass [kg/kmol]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    T_K = temperature_C + 273.15

    if measured_sos == 0:
        M = np.nan
    else:
        M = (kappa * Z * R * T_K) / (measured_sos ** 2)
        M = M * 1e3  # Convert from kg/mol to kg/kmol

    return M


def Z_from_sos_kappa(measured_sos, kappa, molar_mass, temperature_C, R=8.3144621):
    '''
    Calculate compressibility factor Z from measured speed of sound, isentropic exponent, molar mass, and temperature.
    Based on the principles described in [1]_ from GFMW2024.

    Parameters
    ----------
    measured_sos : float
        Measured speed of sound [m/s]
    kappa : float
        Isentropic exponent calculated by appropriate equation of state [-]
    molar_mass : float
        Molar mass [kg/kmol]
    temperature_C : float
        Temperature [C]
    R : float, optional
        Universal gas constant [J/(mol·K)]. Default is 8.3144621 (GERG-2008).

    Returns
    -------
    Z : float
        Compressibility factor [-]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    T_K = temperature_C + 273.15
    M_kg_per_mol = molar_mass / 1e3  # Convert kg/kmol to kg/mol

    if kappa == 0 or R == 0 or T_K == 0:
        Z = np.nan
    else:
        Z = (measured_sos ** 2) * M_kg_per_mol / (kappa * R * T_K)

    return Z

def properties_from_sos_kappa(gas_composition, measured_sos, pressure_bara, temperature_C, EOS='GERG-2008'):
    '''
    Calculate gas properties (density, molar mass, compressibility factor) from measured speed of sound,
    using the relationship between speed of sound, density, and isentropic exponent.

    This function uses an equation of state (EOS) to calculate kappa and Z at the given conditions,
    then applies these to determine the properties from the measured speed of sound.

    Parameters
    ----------
    gas_composition : dict
        Gas composition dictionary with component names as keys and mole percent or mole fraction as values.
        Uses the same format as AGA8 (C1, N2, CO2, C2, C3, iC4, nC4, iC5, nC5, nC6, etc.)
    measured_sos : float
        Measured speed of sound [m/s]
    pressure_bara : float
        Pressure [bara]
    temperature_C : float
        Temperature [C]
    EOS : str, optional
        Equation of state to use. Either 'GERG-2008' or 'DETAIL'. Default is 'GERG-2008'.

    Returns
    -------
    output : dict
        Dictionary containing:
            'rho' : Mass density calculated from measured speed of sound [kg/m3]
            'mm' : Molar mass calculated from measured speed of sound [kg/kmol]
            'z' : Compressibility factor calculated from measured speed of sound [-]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, 
           Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''

    output = {
        'rho' : np.nan,
        'mm' : np.nan,
        'z' : np.nan
    }

    # Use caching to avoid re-initializing the AGA8 object for performance
    # This is important for Monte Carlo simulations or repeated calls
    if not hasattr(properties_from_sos_kappa, '_cached_data'):
        properties_from_sos_kappa._cached_data = {}
    
    # Check if we have a cached AGA8 object for this EOS
    if EOS not in properties_from_sos_kappa._cached_data:
        # Initialize AGA8 object for the specified equation of state
        from pvtlib import aga8
        properties_from_sos_kappa._cached_data[EOS] = aga8.AGA8(EOS)
    
    # Get the cached AGA8 object
    eos_adapter = properties_from_sos_kappa._cached_data[EOS]
    
    # Calculate gas properties using the equation of state
    eos_properties = eos_adapter.calculate_from_PT(
        composition=gas_composition,
        pressure=pressure_bara,
        temperature=temperature_C,
        pressure_unit='bara',
        temperature_unit='C'
    )
    
    # Extract the calculated properties from EOS
    kappa_eos = eos_properties['kappa']  # Isentropic exponent from EOS
    Z_eos = eos_properties['z']          # Compressibility factor from EOS
    M_eos = eos_properties['mm']         # Molar mass from EOS [g/mol], need to convert to kg/kmol
    
    # Calculate density from measured speed of sound and EOS kappa
    output['rho'] = density_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa_eos,
        pressure_bara=pressure_bara
    )
    
    # Calculate molar mass from measured speed of sound and EOS properties
    output['mm'] = molar_mass_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa_eos,
        Z=Z_eos,
        temperature_C=temperature_C
    )
    
    # Calculate compressibility factor from measured speed of sound and EOS properties
    # Note: M_eos is in g/mol, need to convert to kg/kmol (multiply by 1)
    output['z'] = Z_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa_eos,
        molar_mass=M_eos,  # AGA8 returns mm in g/mol, which equals kg/kmol numerically
        temperature_C=temperature_C
    )
    
    return output



