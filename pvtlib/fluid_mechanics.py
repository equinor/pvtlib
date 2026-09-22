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

GRAVITATIONAL_ACCELERATION = 9.80665  # Standard acceleration of free fall g_n [m/s2], NIST SP 811 Appendix B.8. https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8

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


def froude_number(v, D):
    """
    Calculate the ratio of flow velocity to the gravity-wave velocity scale.

    Parameters
    ----------
    v : float
        Non-negative characteristic velocity [m/s].
    D : float
        Positive characteristic length; inner diameter for pipe flow [m].

    Returns
    -------
    Fr : float
        Froude number, ``v / sqrt(g * D)`` [-]. NaN for non-finite or
        non-physical input. Zero velocity gives zero.

    Notes
    -----
    Uses the standard acceleration of free fall, g_n = 9.806 65 m/s2
    exactly [1]_. This is the ordinary Froude number, not the
    density-weighted Froude number used in gas-liquid flow correlations.

    References
    ----------
    .. [1] NIST Special Publication 811, Appendix B.8, "acceleration of
       free fall, standard (g_n)".
       https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8
    """
    if not np.all(np.isfinite([v, D])) or v < 0 or D <= 0:
        return np.nan

    return v / np.sqrt(GRAVITATIONAL_ACCELERATION * D)


def densimetric_froude_number(v, D, rho_phase, rho_other):
    """
    Calculate the lighter phase's density-weighted Froude number.

    Compares inertia of the lighter phase with the buoyancy velocity scale.
    The same definition is used by the wet-gas venturi and USM corrections.

    Parameters
    ----------
    v : float
        Non-negative superficial velocity of the lighter phase [m/s].
    D : float
        Positive inner pipe diameter [m].
    rho_phase : float
        Positive density of the lighter phase, normally gas [kg/m3].
    rho_other : float
        Density of the heavier phase, greater than ``rho_phase`` [kg/m3].

    Returns
    -------
    Fr : float
        ``v / sqrt(g * D) * sqrt(rho_phase / (rho_other - rho_phase))``
        [-]. NaN for non-finite or non-physical input.

    Notes
    -----
    Uses the standard acceleration of free fall, g_n = 9.806 65 m/s2
    exactly [3]_. The velocity is superficial, not the in-situ phase
    velocity. This definition does not cover a phase denser than its
    surroundings; no absolute density difference is substituted.

    References
    ----------
    .. [1] Reader-Harris and Graham, "An improved model for venturi-tube
       overreading in wet gas", NSFMW, 2009.
    .. [2] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equation (7).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    .. [3] NIST Special Publication 811, Appendix B.8, "acceleration of
       free fall, standard (g_n)".
       https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8
    """
    if (not np.all(np.isfinite([v, D, rho_phase, rho_other]))
            or v < 0 or D <= 0 or rho_phase <= 0 or rho_other <= rho_phase):
        return np.nan

    # Apply the buoyancy density scaling to the ordinary Froude number.
    return froude_number(v, D) * np.sqrt(rho_phase / (rho_other - rho_phase))


def weber_number(rho, v, D, surface_tension):
    """
    Calculate the ratio of inertial to surface-tension effects.

    Parameters
    ----------
    rho : float
        Positive density of the phase [kg/m3].
    v : float
        Non-negative characteristic velocity [m/s].
    D : float
        Positive characteristic length [m].
    surface_tension : float
        Positive interfacial tension [N/m].

    Returns
    -------
    We : float
        Weber number, ``rho * v**2 * D / surface_tension`` [-].
        NaN for non-finite or non-physical input.

    Notes
    -----
    For the gas-liquid pipe-flow definition used in the Van Putten model,
    use gas density, superficial gas velocity and inner pipe diameter.
    """
    if (not np.all(np.isfinite([rho, v, D, surface_tension]))
            or rho <= 0 or v < 0 or D <= 0 or surface_tension <= 0):
        return np.nan

    return rho * v**2 * D / surface_tension


def ohnesorge_number(mu, rho, D, surface_tension):
    """
    Calculate the viscous-to-inertial/capillary scale ratio.

    Parameters
    ----------
    mu : float
        Positive dynamic viscosity of the phase [Pa.s].
    rho : float
        Positive density of the same phase [kg/m3].
    D : float
        Positive characteristic length [m].
    surface_tension : float
        Positive interfacial tension [N/m].

    Returns
    -------
    Oh : float
        Ohnesorge number, ``mu / sqrt(rho * surface_tension * D)``
        [-]. NaN for non-finite or non-physical input.

    Notes
    -----
    Independent of velocity. Equals ``sqrt(We) / Re`` when We and Re use
    the same properties, length and non-zero velocity. Use gas properties
    and inner pipe diameter for the Van Putten critical-Froude correlation.
    """
    if (not np.all(np.isfinite([mu, rho, D, surface_tension]))
            or mu <= 0 or rho <= 0 or D <= 0 or surface_tension <= 0):
        return np.nan

    return mu / np.sqrt(rho * surface_tension * D)


def density_ratio(rho_gas, rho_liquid):
    """
    Calculate the gas-to-liquid density ratio at the same conditions.

    Parameters
    ----------
    rho_gas : float
        Positive gas density [kg/m3].
    rho_liquid : float
        Positive liquid density [kg/m3].

    Returns
    -------
    DR : float
        ``rho_gas / rho_liquid`` [-]. NaN for non-finite or non-positive
        densities. No pressure is inferred from this ratio.
    """
    if (not np.all(np.isfinite([rho_gas, rho_liquid]))
            or rho_gas <= 0 or rho_liquid <= 0):
        return np.nan

    return rho_gas / rho_liquid


def lockhart_martinelli_from_GVF(GVF, density_liquid, density_gas):
    """
    Calculate liquid loading X from the flowing gas volume fraction.

    Parameters
    ----------
    GVF : float
        ``Q_gas / (Q_gas + Q_liquid)`` at line conditions [-], in (0, 1].
        This is a flow fraction, not the in-situ gas void fraction.
    density_liquid : float
        Positive liquid density at line conditions [kg/m3].
    density_gas : float
        Positive gas density at the same conditions [kg/m3].

    Returns
    -------
    X : float
        Lockhart-Martinelli parameter [-]. Zero for dry gas (GVF = 1).
        NaN for non-finite or non-physical input.

    Notes
    -----
    Equivalent to ``((1 - GVF) / GVF) * sqrt(density_liquid / density_gas)``.
    Reuses the mass-flow definition rather than maintaining a second X
    correlation for volume-based meters.

    See Also
    --------
    lockhart_martinelli_parameter : Mass-flow definition of X.
    GVF_from_lockhart_martinelli : Inverse conversion.
    """
    if (not np.all(np.isfinite([GVF, density_liquid, density_gas]))
            or not 0 < GVF <= 1 or density_liquid <= 0 or density_gas <= 0):
        return np.nan

    # An arbitrary total volume flow of 1 m3/h gives the required mass ratio.
    return lockhart_martinelli_parameter(
        mass_flow_rate_liquid=(1 - GVF) * density_liquid,
        mass_flow_rate_gas=GVF * density_gas,
        density_liquid=density_liquid,
        density_gas=density_gas,
    )


def GVF_from_lockhart_martinelli(X, density_liquid, density_gas):
    """
    Convert liquid loading X to the flowing gas volume fraction.

    Parameters
    ----------
    X : float
        Non-negative Lockhart-Martinelli parameter [-].
    density_liquid : float
        Positive liquid density at line conditions [kg/m3].
    density_gas : float
        Positive gas density at the same conditions [kg/m3].

    Returns
    -------
    GVF : float
        ``1 / (1 + X * sqrt(density_gas / density_liquid))`` [-].
        NaN for non-finite or non-physical input.

    See Also
    --------
    lockhart_martinelli_from_GVF : Forward conversion.
    """
    if (not np.all(np.isfinite([X, density_liquid, density_gas]))
            or X < 0 or density_liquid <= 0 or density_gas <= 0):
        return np.nan

    return 1 / (1 + X * np.sqrt(density_gas / density_liquid))


def gas_liquid_interfacial_tension_linear_mixing(WLR, surface_tension_oil, surface_tension_water):
    """
    Estimate gas-liquid interfacial tension by simplified volume-split weighting.

    Parameters
    ----------
    WLR : float
        Water volume flow / total oil-water volume flow [-], in [0, 1].
        Volume flows must refer to the same line conditions.
    surface_tension_oil : float
        Positive gas-oil interfacial tension at line conditions [N/m].
    surface_tension_water : float
        Positive gas-water interfacial tension at the same conditions [N/m].

    Returns
    -------
    surface_tension : float
        Approximate gas-liquid interfacial tension [N/m], weighted by the
        oil-water liquid volumetric-flow split.
        NaN for non-finite or non-physical input.

    Notes
    -----
    This is a simplified linear mixing rule, not a general method for
    calculating the interfacial tension of an oil-water mixture against gas.
    It implements the approximation in Equation (43) of [1]:

    ``surface_tension = (1 - WLR) * surface_tension_oil + WLR * surface_tension_water``

    The weights are the oil and water fractions of the total liquid volume
    flow: ``1 - WLR`` and ``WLR``, respectively. They are not mass fractions
    or in-situ liquid holdups. The rule assumes that the two supplied
    gas-liquid interfacial tensions can be combined linearly; applicability
    to the actual fluid system must be assessed separately.
    Both supplied tensions must be positive, even at the pure-component
    endpoints.

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equation (43).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    if (not np.all(np.isfinite([WLR, surface_tension_oil, surface_tension_water]))
            or not 0 <= WLR <= 1 or surface_tension_oil <= 0 or surface_tension_water <= 0):
        return np.nan

    # Weight the gas-oil and gas-water tensions by the liquid volumetric-flow split.
    return (1 - WLR) * surface_tension_oil + WLR * surface_tension_water


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

    If ContaminantVolP is zero, the function returns the measured_total_density.

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
        If ContaminantVolP is zero, returns measured_total_density.

    '''
    
    Contaminant_alpha = ContaminantVolP / 100

    # Check for division by zero error, in which the function will return nan
    if (1 - Contaminant_alpha) == 0:
        Density_dominant_corr = np.nan
    elif Contaminant_alpha == 0:
        Density_dominant_corr = measured_total_density
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