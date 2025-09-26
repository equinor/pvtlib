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

from math import pi
import numpy as np

def reynolds_number(rho: float, v: float, D: float, mu: float) -> float:
    '''
    Calculate Reynolds number for a fluid flow.
    
    Parameters
    ----------
    rho : float
        Fluid density [kg/m3].
    v : float
        Fluid velocity [m/s].
    D : float
        Inner pipe diameter [m].
    mu : float
        Fluid dynamic viscosity [Pa⋅s].

    Returns
    -------
    Re : float
        Reynolds number [-].

    '''
    
    if rho <= 0 or v <= 0 or D <= 0 or mu <= 0:
        return np.nan
    
    Re = rho * v * D / mu
    
    return Re


def superficial_velocity(Q_phase, D):
    '''
    Calculates superficial velocity of a phase
    
    Parameters
    ----------
    Q_phase : float
        Volume flow rate of the phase [m3/h].
    D : float
        Inner pipe diameter [m].

    Returns
    -------
    Us : float
        Superficial velcotiy of the phase [m/s]

    '''
    
    A = pi * ((D/2)**2)
    
    if A==0:
        Us = np.nan
    else:
        Us = (Q_phase/3600) / A

    return Us


def mixture_density_homogeneous(volume_fractions, densities):
    '''
    Calculate the density of a mixture of fluids or components assuming a homogeneous mixture (no slip between phases/components and no interaction between phases/components).
    The volume fractions do not need to sum to 1, as they will be normalized in the function. 
    This allows for easy use of volume fractions given in percentage (0-100 %) or with volume flowrates as direct input.

    Parameters
    ----------
    volume_fractions : list or np.ndarray of float
        Volume fractions of each phase [-].
    densities : list or np.ndarray of float
        Densities of each phase [kg/m3].

    Returns
    -------
    rho_mixture : float
        Mixture density [kg/m3].
    
    '''
    vf = np.array(volume_fractions, dtype=float)
    rho = np.array(densities, dtype=float)

    if vf.shape != rho.shape:
        raise ValueError("Length of volume_fractions and densities must be the same.")

    if np.any(vf < 0):
        return np.nan

    # Filter out phases with zero volume fraction
    non_zero_mask = vf != 0
    vf_active = vf[non_zero_mask]
    rho_active = rho[non_zero_mask]

    # Check if any active phases have invalid densities
    if np.any(rho_active <= 0) or np.any(np.isnan(rho_active)):
        return np.nan

    vf_sum = np.sum(vf_active)
    if vf_sum == 0:
        return np.nan

    vf_normalized = vf_active / vf_sum

    rho_mixture = np.dot(vf_normalized, rho_active)

    return rho_mixture


def GMF_to_GVF(GMF, rho_gas, rho_liquid):
    '''
    Convert from gas mass fraction (GMF) to gas volume fraction (GVF).
    
    Parameters
    ----------
    GMF : float
        Gas mass fraction [-].
    rho_gas : float
        Gas density [kg/m3].
    rho_liquid : float
        Liquid density [kg/m3].
    
    Returns
    -------
    GVF : float
        Gas volume fraction [-].
    '''
    if GMF < 0 or GMF > 1 or rho_gas <= 0 or rho_liquid <= 0:
        return np.nan
    if GMF == 0:
        return 0.0
    
    GVF = 1 / (1 + ((1 - GMF) / GMF) * (rho_gas / rho_liquid))

    return GVF


def GVF_to_GMF(GVF, rho_gas, rho_liquid):
    '''
    Convert from gas volume fraction (GVF) to gas mass fraction (GMF).

    Parameters
    ----------
    GVF : float
        Gas volume fraction [-].
    rho_gas : float
        Gas density [kg/m3].
    rho_liquid : float
        Liquid density [kg/m3].

    Returns
    -------
    GMF : float
        Gas mass fraction [-].
    '''
    if GVF < 0 or GVF > 1 or rho_gas <= 0 or rho_liquid <= 0:
        return np.nan
    if GVF == 0:
        return 0.0

    GMF = 1 / (1 + ((1 - GVF) / GVF) * (rho_liquid / rho_gas))

    return GMF


def lockhart_martinelli_parameter(mass_flow_rate_liquid, mass_flow_rate_gas, density_liquid, density_gas):
    '''
    Calculate the Lockhart-Martinelli parameter X.

    Note: The units for mass flow rates and densities must be consistent between phases,
    but do not need to be SI units (e.g., both in kg/h and both in kg/m3 are valid).

    Parameters
    ----------
    mass_flow_rate_liquid : float
        Mass flow rate of liquid phase [kg/h or kg/s].
    mass_flow_rate_gas : float
        Mass flow rate of gas phase [kg/h or kg/s].
    density_liquid : float
        Density of liquid phase [kg/m3].
    density_gas : float
        Density of gas phase [kg/m3].

    Returns
    -------
    X : float
        Lockhart-Martinelli parameter [-].
    '''

    if mass_flow_rate_gas <= 0 or density_gas <= 0 or density_liquid <= 0:
        return np.nan

    X = (mass_flow_rate_liquid / mass_flow_rate_gas) * ((density_gas / density_liquid) ** 0.5)

    return X


def liquid_holdup_from_density(measured_density, liquid_density, gas_density):
    '''
    Based on a measured mix density and liquid and gas densities, calculate liquid hold-up.
    Assuming no slip between gas and liquid.
    
    If measured density is higher then liquid density, return 1 in liquid hold-up. 
    If measured density is lower then gas density, return 0 in liquid hold-up.

    Parameters
    ----------
    measured_density : float
        Measured mix density [kg/m3]
    liquid_density : float
        Liquid density [kg/m3]
    gas_density : float
        Gas density [kg/m3]

    Returns
    -------
    liquid holdup, float
        Liquid holdup fraction, assuming no slip [-].

    '''
    
    if measured_density>liquid_density:
        return 1.0
    
    if measured_density<gas_density:
        return 0.0
    
    if liquid_density==gas_density:
        return np.nan
    else:
        return (measured_density-gas_density)/(liquid_density-gas_density)
    
    
    
#%% Equations used to evaluate the critical velocity (minimum velocity) required to achieve a uniform dispersion of water in oil

def critical_velocity_for_uniform_wio_dispersion_horizontal(ST_oil_aq, rho_o, rho_aq, Visc_o, D, K1=2.02, G=10):
    '''
    Calculate critical (minimum) velocity for maintaining a dispersion degree G, based on NFOGM HANDBOOK of Water Fraction Metering [1_].
    
    The value G = 10 gives a concentration ratio 0.9, and is recommended by ISO 3171. This corresponds to ±5 % deviation from the mean concentration and it is in
    practise considered as a homogeneous mixture.
    
    The numerical constant K1 depends on the unit system being used, and the default K1 corresponds to SI units, which is being used in this function.
    The function will also work for field SI units (K1 = 0.5), but the units will no longer be valid. 
    
    The method described here should be used with care since it is based on a simplified
    concentration model, as well as other simplified and semi-theoretical models. The
    water concentration model is only valid for small water volume fractions, i.e. less
    than approximately 10–15 % water in oil. 
    
    Equation and info from NFOGM HANDBOOK of Water Fraction Metering (Revision 2, December 2004), chapter 5.1, Equation 2. 

    Parameters
    ----------
    ST_oil_aq : float
        Interfacial (surface) tension between oil and water [N/m].
    rho_o : float
        Oil density [kg/m3].
    rho_aq : float
        Aqueous density [kg/m3].
    Visc_o : float
        Oil viscosity [Pa⋅s].
    D : float
        Inner pipe diameter [m].
    K1 : float
        Constant depending on unit system (SI or field units) The default is 2.02 which corresponds to SI units.
    G : float, optional
        Parameter defining the degree of dispersion (usually G = 10). The default is 10.

    Returns
    -------
    Vc : float
        Critical (minimum) velocity for maintaining a dispersion degree G [m/s].

    References
    ----------
    .. [1] NFOGM, Handbook of Water Fraction Metering. Revision 2 ed. 2004
    '''
    

    if rho_o == 0 or Visc_o == 0:
        Vc = np.nan
    else:
        Vc = K1 * (G ** 0.325) * (ST_oil_aq ** 0.39) * (((rho_aq - rho_o) ** 0.325) / (rho_o ** 0.283)) * ((D ** 0.366) / (Visc_o ** 0.431))    
    
    return  Vc

   
def critical_velocity_for_uniform_wio_dispersion_vertical(beta, ST_oil_aq, rho_o, rho_aq, Visc_o, D, K2=2910):
    '''
    Calculate the critical (minimum) velocity Vc which is required to maintain a homogeneous flow in a vertical, or inclined pipe, based on NFOGM HANDBOOK of Water Fraction Metering [1_].
    The numerical constant K2 depends on the unit system being used and the default K2 corresponds to SI units, which is being used in this function.
    The function will also work for field SI units (K2 = 550), but the units will no longer be valid. 

    This model is valid for vertical and inclined pipe flow (45° - 90° from the horizontal plane).
    Furthermore, the model is valid for low to moderate high water concentrations, i.e.
    20 – 25 %. 

    Equation and info from NFOGM HANDBOOK of Water Fraction Metering (Revision 2, December 2004), chapter 5.1, Equation 9. 

    Parameters
    ----------
    beta : float
        Volumetric water fraction in per cent [vol%].
    ST_oil_aq : float
        Interfacial (surface) tension between oil and water [N/m].
    rho_o : float
        Oil density [kg/m3].
    rho_aq : float
        Aqueous density [kg/m3].
    Visc_o : float
        Oil viscosity [Pa⋅s].
    D : float
        Inner pipe diameter [m].
    K2 : float
        Constant depending on unit system (SI or field units) The default is 2910 which corresponds to SI units.

    Returns
    -------
    Vc : float
        Critical (minimum) velocity Vc which is required to maintain a homogeneous flow in a vertical, or inclined pipe [m/s].
    
    References
    ----------
    .. [1] NFOGM, Handbook of Water Fraction Metering. Revision 2 ed. 2004
    '''
    
    if rho_o == 0 or Visc_o == 0 or beta >= 100 or beta<0:
        Vc = np.nan
    else:
        Vc = K2 * ((beta ** 0.556) / ((100 - beta) ** 1.556)) * (ST_oil_aq ** 0.278) * (((rho_aq - rho_o) ** 0.278) / (rho_o ** 0.444)) * ((D / Visc_o) ** 0.111)
    
    return Vc

'''
Equations for convering between volume percent and mass percent in a two-phase system and for correcting a mixed density for the presence of a contaminant
The following calculations assumes a mixture of two immiscible liquids with a known density for each phase. If used for a fluid flow scenario, it also assumes no slip between the phases. 
i.e.    rho_mix = rho_A * alpha_A + rho_B * alpha_B
These equations are typically useful in "oil-in-water" and "water-in-oil" systems. 

Nomenclature:
    Dominant phase - The continuous phase, e.g for normal operation the oil phase is the Dominant phase (continous phase) in an oil metering station.
    Contaminant phase - The disperse phase, e.g for normal operation any water present in an oil metering station is the Contaminant(disperse phase) in that oil metering station. 
'''

def volume_percent_to_mass_percent(ContaminantVolP, DominantPhase_EOS_density, ContaminantPhase_EOS_density):
    '''
    Convert from volume percentage to mass percentage
    The EOS density can be calculated from an equation of state, or from another source, as long as it represents the density of the dominant and contaminant phases.
    
    Parameters
    ----------
    ContaminantVolP : float
        Volume percentage, contaminant phase [%]
    DominantPhase_EOS_density : float
        Calculated denstiy from equation of state, dominant phase [kg/m3]
    ContaminantPhase_EOS_density : float
        Calculated denstiy from equation of state, contaminant phase [kg/m3]
        
    Returns
    -------
    ContaminantMassP: float
        Mass percentage, contaminant phase [%]
        
    '''

    Contaminant_alpha = ContaminantVolP / 100
    
    # Check for division by zero error, in which the function will return nan
    if ContaminantPhase_EOS_density == 0.0 or DominantPhase_EOS_density == 0.0:
        Contaminant_omega = np.nan
    else:
        Contaminant_omega = (Contaminant_alpha * ContaminantPhase_EOS_density) / (((1 - Contaminant_alpha) * DominantPhase_EOS_density) +
                    (Contaminant_alpha * ContaminantPhase_EOS_density))
    ContaminantMassP = Contaminant_omega * 100
    
    return ContaminantMassP


def mass_percent_to_volume_percent(ContaminantMassP, DominantPhase_EOS_density, ContaminantPhase_EOS_density):
    '''
    Convert from mass percentage to volume percentage
    The EOS density can be calculated from an equation of state, or from another source, as long as it represents the density of the dominant and contaminant phases.
    
    Parameters
    ----------
    ContaminantMassP : float
        Mass percentage, contaminant phase [%]
    DominantPhase_EOS_density : float
        Calculated denstiy from equation of state, dominant phase [kg/m3]
    ContaminantPhase_EOS_density : kg/m3
        Calculated denstiy from equation of state, contaminant phase [kg/m3]

    Returns
    -------
    ContaminantVolP: float
        Volume percentage, contaminant phase [%]

    '''
    
    # Check for division by zero error, in which the function will return nan
    if ContaminantPhase_EOS_density == 0.0 or DominantPhase_EOS_density == 0.0:
        ContaminantVolP =np.nan
    else:
        Contaminant_omega = ContaminantMassP / 100
        Contaminant_alpha = Contaminant_omega / ContaminantPhase_EOS_density / (
                    Contaminant_omega / ContaminantPhase_EOS_density +
                    (1 - Contaminant_omega) / DominantPhase_EOS_density)
        ContaminantVolP = Contaminant_alpha * 100
    
    return ContaminantVolP


def dominant_phase_corrected_density(measured_total_density, ContaminantVolP, ContaminantPhase_EOS_density):    
    '''
    Use measured total density (for example from a coriolis meter) to estimate a "measured" density of the dominant phase corrected for contamination, 
    i.e. the density with the contaminant phase removed.
    The EOS density can be calculated from an equation of state, or from another source, as long as it represents the density of the dominant and contaminant phases.

    Example of usage: What is the density of the oil phase if the measured density is 800 kg/m3 and the water fraction is 1vol%?
    
    Parameters
    ----------
    measured_total_density : float
        Measured total density, i.e. density including both dominant and contaminant phase [kg/m3]
    ContaminantVolP : float
        Volume percentage, contaminant phase [%]
    ContaminantPhase_EOS_density : float
        Calculated denstiy from equation of state, contaminant phase [kg/m3]

    Returns
    -------
    Density_dominant_corr : float
        Estimated density of the dominant phase, based on measured density, corrected for contaminant phase [kg/m3]

    '''
    
    Contaminant_alpha = ContaminantVolP / 100

    # Check for division by zero error, in which the function will return nan
    if (1 - Contaminant_alpha) == 0:
        Density_dominant_corr = np.nan
    else:
        Density_dominant_corr = (measured_total_density - ContaminantPhase_EOS_density * Contaminant_alpha) / (
                    1 - Contaminant_alpha)
    
    return Density_dominant_corr


def contaminant_volume_percent_from_mixed_density(measured_total_density, DominantPhase_EOS_density, ContaminantPhase_EOS_density):
    '''
    Calculate the fraction of contaminant phase in a two-phase system, based on a measured total density and the densities of the two phases.
    The EOS density can be calculated from an equation of state, or from another source, as long as it represents the density of the dominant and contaminant phases.

    Example of usage: What is the water fraction if the measured density is 850 kg/m3, the oil density is 800 kg/m3 and the water density is 1000 kg/m3?
    
    Parameters
    ----------
    measured_total_density : float
        Measured total density, i.e. density including both dominant and contaminant phase [kg/m3]
    DominantPhase_EOS_density : float
        Calculated denstiy from equation of state, dominant phase [kg/m3]
    ContaminantPhase_EOS_density : float
        Calculated denstiy from equation of state, contaminant phase [kg/m3]

    Returns
    -------
    ContaminantVolP : float
        Volume percentage, contaminant phase [%]
    '''
    
    # Check for division by zero error, in which the function will return nan
    if DominantPhase_EOS_density == ContaminantPhase_EOS_density:
        ContaminantVolP = np.nan
    else:
        Contaminant_alpha = (measured_total_density - DominantPhase_EOS_density) / (ContaminantPhase_EOS_density - DominantPhase_EOS_density)
        ContaminantVolP = Contaminant_alpha * 100
    
    #Check that contaminant volume percentage is within physical limits (0-100 %)
    if ContaminantVolP <= 0:
        ContaminantVolP = 0
    elif ContaminantVolP >= 100:
        ContaminantVolP = 100

    return ContaminantVolP