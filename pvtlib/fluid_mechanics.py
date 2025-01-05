from math import pi
from numpy import nan

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
        Us = nan
    else:
        Us = (Q_phase/3600) / A

    return Us
   

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
        return nan
    else:
        return (measured_density-gas_density)/(liquid_density-gas_density)
    
    
    
#%% Equations used to evaluate the critical velocity (minimum velocity) required to achieve a uniform dispersion of water in oil

def critical_velocity_for_uniform_wio_dispersion_horizontal(ST_oil_aq, rho_o, rho_aq, Visc_o, D, K1=2.02, G=10):
    '''
    Calculate critical (minimum) velocity for maintaining a dispersion degree G.
    
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

    '''
    

    if rho_o == 0 or Visc_o == 0:
        Vc = nan
    else:
        Vc = K1 * (G ** 0.325) * (ST_oil_aq ** 0.39) * (((rho_aq - rho_o) ** 0.325) / (rho_o ** 0.283)) * ((D ** 0.366) / (Visc_o ** 0.431))    
    
    return  Vc

   
def critical_velocity_for_uniform_wio_dispersion_vertical(Betha, ST_oil_aq, rho_o, rho_aq, Visc_o, D, K2=2910):
    '''
    Calculate the critical (minimum) velocity Vc which is required to maintain a homogeneous flow in a vertical, or inclined pipe. 
    The numerical constant K2 depends on the unit system being used and the default K2 corresponds to SI units, which is being used in this function.
    The function will also work for field SI units (K2 = 550), but the units will no longer be valid. 

    This model is valid for vertical and inclined pipe flow (45° - 90° from the horizontal plane).
    Furthermore, the model is valid for low to moderate high water concentrations, i.e.
    20 – 25 %. 

    Equation and info from NFOGM HANDBOOK of Water Fraction Metering (Revision 2, December 2004), chapter 5.1, Equation 9. 

    Parameters
    ----------
    Betha : float
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
    '''
    
    if rho_o == 0 or Visc_o == 0 or Betha == 100 or Betha<0:
        Vc = nan
    else:
        Vc = K2 * ((Betha ** 0.556) / ((100 - Betha) ** 1.556)) * (ST_oil_aq ** 0.278) * (((rho_aq - rho_o) ** 0.278) / (rho_o ** 0.444)) * ((D / Visc_o) ** 0.111)
    
    return Vc