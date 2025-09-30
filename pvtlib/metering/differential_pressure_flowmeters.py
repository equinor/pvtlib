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
from math import sqrt, pi, e

from pvtlib.fluid_mechanics import (
    reynolds_number as _reynolds_number,
    superficial_velocity as _superficial_velocity,
    lockhart_martinelli_parameter as _lockhart_martinelli_parameter,
    GVF_to_GMF as _GVF_to_GMF
)

def _calculate_flow_DP_meter(C, D, d, epsilon, dP, rho1):
    """
    Calculate the mass flow rate through a differential pressure (DP) meter.
    This formula is given as "Formula (1)" in ISO 5167 part 2 [1]_ and 4 [2]_ (2022 edition),
    and is valid for orifice plates and Venturi tubes.

    Parameters
    ----------
    C : float
        Discharge coefficient of the meter.
    D : float
        Diameter of the pipe [m].
    d : float
        Diameter of the throat [m].
    epsilon : float
        Expansion factor.
    dP : float
        Differential pressure across the meter [mbar].
    rho1 : float
        Density of the fluid [kg/m3].

    Returns
    -------
    results : dict
        Dictionary containing the following keys:
        - 'MassFlow': Mass flow rate [kg/h].
        - 'VolFlow': Volume flow rate [m3/h].
        - 'Velocity': Flow velocity [m/s].
    
    References
    ----------
    .. [1] ISO 5167-2:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 2: Orifice plates.
    .. [2] ISO 5167-4:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 4: Venturi tubes.
    """
    
    results = {}

    dP_Pa = dP * 100  # Convert mbar to Pa

    # Calculate beta
    beta = calculate_beta_DP_meter(D, d)

    # Calculate mass flowrate in kg/h
    results['MassFlow'] = (C/sqrt(1 - (beta**4)))*epsilon*(pi/4)*((d)**2)*sqrt(2*dP_Pa*rho1)*3600 # kg/h

    # Calculate volume flowrate in m3/h
    results['VolFlow'] = results['MassFlow']/rho1 # m3/h

    # Calculate velocity in m/s
    results['Velocity'] = _superficial_velocity(results['VolFlow'], D) # m/s

    return results


#%% Venturi equations
def calculate_flow_venturi(D, d, dP, rho1, C=None, epsilon=None, check_input=False):
    '''
    Calculate the flow rates (mass flow, volume flow, and velocity) through a Venturi meter.
    Calculations performed according to ISO 5167-4:2022 [1_]. 

    If discharge coefficient is not provided, the function uses the value of 0.984 given in ISO 5167-4:2022 for "as cast" Venturi tubes. 

    Parameters
    ----------
    D : float
        Diameter of the pipe (must be greater than zero). [m]
    d : float
        Diameter of the throat (must be greater than zero). [m]
    dP : float
        Differential pressure (must be greater than zero). [mbar]
    rho1 : float
        Density of the fluid (must be greater than zero). [kg/m3]
    C : float, optional
        Discharge coefficient (default is 0.984). [-]
    epsilon : float, optional
        Expansion factor (default is None). [-]
    check_input : bool, optional
        If True, the function will raise an exception if any of the input parameters are invalid.
        The default value is False, and the reason is to prevent the function from running into an exception if the input parameters are invalid. 

    Returns
    -------
    results : dict
        Dictionary containing the following keys:
        - 'MassFlow': Mass flow rate [kg/h].
        - 'VolFlow': Volume flow rate [m3/h].
        - 'Velocity': Flow velocity [m/s].
        - 'C': Discharge coefficient used.
        - 'epsilon': Expansion factor used.

    Raises
    ------
    Exception
        If any of the input parameters are invalid (negative or zero where not allowed).
    
    References
    ----------
    .. [1] ISO 5167-4:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 4: Venturi tubes.
    '''
    
    # Dictionary containing all results from calculations
    results = {
        'MassFlow': np.nan,
        'VolFlow': np.nan,
        'Velocity': np.nan,
        'C': np.nan,
        'epsilon': np.nan
        }
    
    if check_input:
        if D <= 0.0:
            raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')
        if d <= 0.0:
            raise Exception('ERROR: Negative diameter input. Diameter (d) must be a float greater than zero')
        if dP <= 0.0:
            raise Exception('ERROR: Negative differential pressure input. Differential pressure (dP) must be a float greater than zero')
    else:    
        if D <= 0.0:
            return results
        if rho1 <= 0.0:
            return results
        if dP < 0.0:
            return results

    if C is None:
        C_used = 0.984
    else:
        C_used = C

    if epsilon is None:
        epsilon_used = 1.0
    else:
        epsilon_used = epsilon
    
    # Calculate diameter ratio (beta) of the Venturi meter
    beta = calculate_beta_DP_meter(D, d)

    # Calculate flowrates
    results = _calculate_flow_DP_meter(
        D=D,
        d=d,
        C=C_used,
        epsilon=epsilon_used,
        dP=dP,
        rho1=rho1
        )

    # Return epsilon used and discharge coefficient used
    results['C'] = C_used
    results['epsilon'] = epsilon_used

    return results


def calculate_expansibility_venturi(P1, dP, beta, kappa):
    '''
    Calculate the expansibility factor for a Venturi meter [1]_.

    Parameters
    ----------
    P1 : float
        Upstream pressure. [bara]
    dP : float
        Differential pressure. [mbar]
    beta : float
        Diameter ratio (d/D). [-]
    kappa : float
        Isentropic exponent. [-]

    Returns
    -------
    epsilon : float
        Expansibility factor. [-]
    
    References
    ----------
    .. [1] ISO 5167-4:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 4: Venturi tubes.
    '''

    # Calculate pressure ratio
    P2 = P1 - (dP/1000) # Convert dP from mbar to bar
    tau = P2/P1

    # Isentropic exponent cannot be equal to 1, as it would result in division by zero. Return NaN in this case.
    if kappa==1:
        return np.nan

    # Calculate expansibility factor
    epsilon = sqrt((kappa*tau**(2/kappa)/(kappa-1))*((1-beta**4)/(1-beta**4*tau**(2/kappa)))*(((1-tau**((kappa-1)/kappa))/(1-tau))))

    return epsilon


def calculate_beta_DP_meter(D, d):
    '''
    Calculate the diameter ratio (beta) for a traditional DP based meter, such as venturi and orifice plates.
    Calculation according to ISO 5167:2022 (part 1,2,4) [1]_.

    Parameters
    ----------
    D : float
        The diameter of the pipe at the upstream tapping(s). Must be greater than zero.
    d : float
        The diameter of the throat.
    Returns
    -------
    beta : float
        The beta ratio (d/D).
    Raises
    ------
    Exception
        If the diameter of the pipe (D) is less than or equal to zero.
    
    Notes
    -----
    This function cannot be used for cone meters, as the diameter ratio is defined differently (see calculate_beta_V_cone).  

    References
    ----------
    .. [1] ISO 5167-1:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 1: General principles and requirements.
    '''
    
    if D<=0.0:
        raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')

    beta = d/D
    
    return beta



#%% V-cone equations
def calculate_flow_V_cone(D, beta, dP, rho1, C = None, epsilon = None, check_input=False):
    '''
    Calculate mass flowrate and volume flowrate of a V-cone meter. 
    Calculations performed according to NS-EN ISO 5167-5:2022 [1]_. 

    Parameters
    ----------
    D : float
        The diameter of the pipe at the beta edge, D.  [m]
        Assumes that the diameter of the pipe at the upstream tapping, DTAP, is equal to the diameter of the pipe at the beta edge, D. 
        In easier terms, its the inlet diameter.
    beta : float
        V-cone beta.
    dP : float
        Differential pressure [mbar].
    rho1 : float
        Density at the upstream tapping [kg/m3].
    C : float, optional
        Discharge coefficient. 
        If no value of C is provided, the function uses the value of 0.82 given in NS-EN ISO 5167-5:2022.
    epsilon : float, optional
        expansibility factor (ε) is a coefficient used to take into account the compressibility of the fluid. 
        If no expansibility is provided, the function will use 1.0. 
    check_input : bool, optional
        If True, the function will raise an exception if any of the input parameters are invalid. 
        The default value is False, and the reason is to prevent the function from running into an exception if the input parameters are invalid.

    Returns
    -------
    results : dict
        Dictionary containing the following keys:
        - 'MassFlow': Mass flow rate [kg/h].
        - 'VolFlow': Volume flow rate [m3/h].
        - 'Velocity': Flow velocity [m/s].
        - 'C': Discharge coefficient used.
        - 'epsilon': Expansion factor used.

    References
    ----------
    .. [1] NS-EN ISO 5167-5:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 5: Cone meters.
    '''
    
    # Dictionary containing all results from calculations
    results = {
        'MassFlow': np.nan,
        'VolFlow': np.nan,
        'Velocity': np.nan,
        'C': np.nan,
        'epsilon': np.nan
    }

    if check_input:
        if D<=0.0:
            raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')
        if rho1<=0.0:
            raise Exception('ERROR: Negative density input. Density (rho1) must be a float greater than zero')
        if dP<0.0:
            raise Exception('ERROR: Negative differential pressure input. Differential pressure (dP) must be a float greater than zero')
    else:
        if D<=0.0:
            return results
        if rho1<=0.0:
            return results
        if dP<0.0:
            return results
    
    if C is None: 
        C_used = 0.82
    else:
        C_used = C
    
    if epsilon is None:
        epsilon_used = 1.0
    else:
        epsilon_used = epsilon
    
    # Convert differential pressure to Pascal
    dP_Pa = dP * 100 # 100 Pa/mbar
    
    # Calculate mass flowrate
    results['MassFlow'] = (C_used/sqrt(1 - (beta**4)))*epsilon_used*(pi/4)*((D*beta)**2)*sqrt(2*dP_Pa*rho1)*3600 # kg/h
    
    # Calculate volume flowrate
    results['VolFlow'] = results['MassFlow']/rho1 # m3/h
            
    # Calculate velocity
    r = D/2
    results['Velocity'] = results['VolFlow']/((pi*(r**2))*3600) # m/s
    
    # Return epsilon used and discharge coefficient used    
    results['C'] = C_used
    results['epsilon'] = epsilon_used
    
    return results


def calculate_expansibility_Stewart_V_cone(beta , P1, dP, k, check_input=False):
    '''
    Calculates the expansibility factor for a cone flow meter
    based on the geometry of the cone meter, measured differential pressures of the V-cone meter
    and the isentropic exponent of the fluid [1]_.

    Parameters
    ----------
    beta : float
        V-cone beta, [-]
    P1 : float
        Static pressure of fluid upstream of cone meter at the cross-section of
        the pressure tap, [bara]
    dP : float
        Differential pressure [mbar]
    k : float
        Isentropic exponent of fluid, [-]

    Returns
    -------
    expansibility : float
        Expansibility factor (1 for incompressible fluids, less than 1 for real fluids) [-]

    Notes
    -----
    This formula was determined for the range of P2/P1 >= 0.75; the only gas
    used to determine the formula is air.

    References
    ----------
    .. [1] Stewart, D., M. Reader-Harris, and R. Peters. Derivation of an expansibility factor for the V-Cone meter. in Flow Measurement International Conference, Peebles, Scotland, UK. 2001.
    '''
    
    dP_Pa = dP*100 # Convert mbar to Pa
    
    P1_Pa = P1*10**5 # Convert bara to Pa
    
    if check_input:
        if P1<=0.0:
            raise Exception('ERROR: Negative pressure input. Pressure (P1) must be a float greater than zero')
        if dP<0.0:
            raise Exception('ERROR: Negative differential pressure input. Differential pressure (dP) must be a float greater than zero')
    else:
        if P1<=0.0:
            return np.nan
        if dP<0.0:
            return np.nan

    epsilon = 1.0 - (0.649 + 0.696*(beta**4))*dP_Pa/(k*P1_Pa)
    
    return epsilon


def calculate_beta_V_cone(D, dc):
    '''
    Calculates V-cone beta according to ISO 5167-5:2022 [1]_.

    beta edge: maximum circumference of the cone

    Parameters
    ----------
    D : float
        The diameter of the pipe at the beta edge, D. 
        Assumes that the diameter of the pipe at the upstream tapping is equal to the diameter of the pipe at the beta edge, D. 
        In easier terms, its the inlet inner diameter. 
        
    dc : float
        dc is the diameter of the cone in the plane of the beta edge [m]. 
        In easier terms, its the outer diameter of the cone. 

    Returns
    -------
    beta : float
        V-cone beta.

    References
    ----------
    .. [1] ISO 5167-5:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 5: Cone meters.
    '''
    
    if D<=0.0:
        raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')

    beta = sqrt(1-((dc**2)/(D**2)))

    return beta


#%% Orifice equations
def calculate_flow_orifice(D, d, dP, rho1, mu=None, C=None, epsilon=None, tapping='corner', check_input=False):
    """
    Calculate the flow rate through an orifice plate according to ISO 5167-2:2022 [1]_.

    Parameters
    ----------
    D : float
        Pipe diameter (m).
    d : float
        Orifice diameter (m).
    dP : float
        Differential pressure across the orifice (mbar).
    rho1 : float
        Fluid density upstream of the orifice (kg/m3).
    mu : float, optional
        Dynamic viscosity of the fluid (Pa*s). Required if `C` is not provided.
    C : float, optional
        Discharge coefficient. If not provided, it will be calculated iteratively.
    epsilon : float, optional
        Expansibility factor. If not provided, 1.0 will be used (valid for incompressible fluids).
    tapping : str, optional
        Tapping type for the orifice plate. Default is 'corner'.
    check_input : bool, optional
        If True, the function will raise exceptions for invalid input parameters. If False, it will return a dictionary with NaN values for invalid inputs.
    Returns
    -------
    results : dict
        Dictionary containing the following keys:
        - 'MassFlow': Mass flow rate [kg/h].
        - 'VolFlow': Volume flow rate [m3/h].
        - 'Velocity': Flow velocity [m/s].
        - 'C': Discharge coefficient used.
        - 'epsilon': Expansion factor used.
        - 'Re': Reynolds number.
    Raises
    ------
    Exception
        If `check_input` is True and any of the input parameters are invalid, or if the iterative calculation for the discharge coefficient does not converge.

    References
    ----------
    .. [1] ISO 5167-2:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 2: Orifice plates.
    """
    
    # Define a dictionary that is returned if the function is called with check_input=False and the input parameters are invalid
    # This is done to preserve the structure of the results dictionary, even if the function is called with invalid input parameters
    results_error = {key : np.nan for key in ['MassFlow', 'VolFlow', 'Velocity', 'C', 'epsilon', 'Re']}

    if check_input:
        if D <= 0.0:
            raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')
        if rho1 <= 0.0:
            raise Exception('ERROR: Negative density input. Density (rho1) must be a float greater than zero')
        if dP < 0.0:
            raise Exception('ERROR: Negative differential pressure input. Differential pressure (dP) must be a float greater than zero')
        if (mu is None) and (C is None):
            raise Exception('ERROR: Either dynamic viscosity (mu) or discharge coefficient (C) must be provided. If C is not given, it is calculated, which requires viscosity as an input.')
    else:
        if D <= 0.0:
            return results_error
        if rho1 <= 0.0:
            return results_error
        if dP < 0.0:
            return results_error
        if (mu is None) and (C is None):
            return results_error

    # If expansibility (epsilon) is not provided, the function will use 1.0, which is valid for incompressible fluids.
    if epsilon is None:
        epsilon_used = 1.0
    else:
        epsilon_used = epsilon


    # If discharge coefficient is provided, flowrates can be calculated directly
    if not C is None:
        C_used = C

        results = _calculate_flow_DP_meter(
            C=C_used, 
            D=D,
            d=d,
            epsilon=epsilon_used,
            dP=dP,
            rho1=rho1
            )
        
        # Calculate Reynolds number
        results['Re'] = _reynolds_number(rho=rho1, v=results['Velocity'], D=D, mu=mu)
        
        return results

    else:
        # Solve for discharge coefficient using iterative calculation
        # Max number of iterations
        max_iter = 100

        # Criteria for convergence
        criteria = 1e-100

        # Initial guess for discharge coefficient
        C_init = 0.5
        C = C_init

        for i in range(max_iter):
            # Perform initial calculation of flowrates
            results = _calculate_flow_DP_meter(
                D=D,
                d=d,
                C=C, 
                epsilon=epsilon_used,
                dP=dP,
                rho1=rho1
            )

            # Calculate Reynolds number
            Re = _reynolds_number(rho=rho1, v=results['Velocity'], D=D, mu=mu)

            # Calculate beta
            beta = calculate_beta_DP_meter(D=D, d=d)

            # Calculate discharge coefficient using Reader-Harris/Gallagher equation
            C_calc = calculate_C_orifice_ReaderHarrisGallagher(D=D, beta=beta, Re=Re, tapping=tapping, check_input=False)

            # Check for convergence
            diff_C = abs(C_calc - C)

            if diff_C < criteria:
                break

            # Update discharge coefficient for next iteration
            C = C_calc
            
        # If the loop completes without convergence, raise an exception
        else:
            if check_input:
                raise Exception(f'ERROR: Iterative calculation for discharge coefficient did not converge in {max_iter} iterations.') 
            else:
                return results_error

        # Add C_used, epsilon_used and reynolds number to results
        results['C'] = C
        results['epsilon'] = epsilon_used
        results['Re'] = Re

        return results


def calculate_expansibility_orifice(P1, dP, beta, kappa):
    '''
    Calculate the expansibility factor for an orifice meter according to ISO 5167-2:2022 [1]_[2]_. 
    The calculation is valid under the criterias given by the standard.

    Parameters
    ----------
    P1 : float
        Upstream pressure. [bara]
    dP : float
        Differential pressure. [mbar]
    beta : float
        Diameter ratio (d/D). [-]
    kappa : float
        Isentropic exponent. [-]

    Returns
    -------
    epsilon : float
        Expansibility factor. [-]
    
    References
    ----------
    .. [1] Reader-Harris, M. The equation for the expansibility factor for orifice plates. in Proceedings of the FLOMEKO. 1998.
    .. [2] ISO 5167-2:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 2: Orifice plates.
    '''

    # Calculate pressure ratio
    P2 = P1 - (dP/1000) # Convert dP from mbar to bar
    tau = P2/P1

    # Isentropic exponent cannot be equal to 1, as it would result in division by zero. Return NaN in this case.
    if kappa==0:
        return np.nan
    # P1 cannot be zero, as it would result in division by zero. Return NaN in this case.
    if P1==0:
        return np.nan  

    # Calculate expansibility factor
    epsilon = 1-(0.351+0.256*(beta**4)+0.93*(beta**8))*(1-(tau**(1/kappa)))

    return epsilon


def calculate_C_orifice_ReaderHarrisGallagher(D, beta, Re, tapping='corner', check_input=False):
    """
    Calculate the discharge coefficient (C) for an orifice plate using the Reader-Harris/Gallagher equation [1]_.
    Calculations performed according to ISO 5167-2:2022 [2]_.
    
    Parameters
    ----------
    D : float
        Pipe diameter in meters.
    beta : float
        Diameter ratio (orifice diameter / pipe diameter).
    Re : float
        Reynolds number.
    tapping : str, optional
        Type of pressure tapping. Options are 'corner', 'D', 'D/2', or 'flange'. Default is 'corner'.
    check_input : bool, optional
        If True, input values are checked for validity. Default is False.
    Returns
    -------
    C : float
        Discharge coefficient (C). Returns NaN if inputs are invalid and `check_input` is False.
    Raises
    ------
    Exception
        If `check_input` is True and any of the inputs are invalid.
    Notes
    -----
    The function converts the pipe diameter to millimeters as required by the Reader-Harris/Gallagher equation.
    The equation includes an additional term for pipe diameters less than 71.12 mm as specified by ISO 5167-1:2022.

    References
    ----------
    .. [1] Reader-Harris, M. and J. Sattary. The orifice plate discharge coefficient equation-the equation for ISO 5167-1. in Proceedings of the 14th North Sea Flow Measurement Workshop, Peebles, UK. 1996.
    .. [2] ISO 5167-2:2022, Measurement of fluid flow by means of pressure differential devices inserted in circular cross-section conduits running full -- Part 2: Orifice plates.
    """


    if check_input:
        if Re <= 0.0:
            raise Exception('ERROR: Negative Reynolds number input. Reynolds number (Re) must be a float greater than zero')
        if type(tapping) != str:
            raise Exception('ERROR: Invalid tapping input. Tapping (tapping) must be a string')
    else:
        if Re==0:
            return np.nan
        if type(tapping) != str:
            return np.nan
    
    # Convert diameter to mm, as required by the Reader-Harris-Gallagher equation
    D_mm=D*1000

    if tapping.lower() == 'corner':
        L1 = 0.0
        L2 = 0.0
    elif tapping.lower() in ['d','d/2']:
        L1 = 1.0
        L2 = 0.47
    elif tapping.lower() == 'flange':
        L1 = 25.4/D_mm
        L2 = 25.4/D_mm
    else:
        if check_input:
            raise Exception('ERROR: Invalid tapping input. Tapping (tapping) must be either "corner", "D", "D/2" or "flange"')
        else:
            return np.nan
    
    M2 = 2*L2/(1-beta)

    A = (19000*beta/Re)**0.8

    # From ISO 5167-1:2022: Where D < 71,12 mm (2,8 in), 
    # the following term shall be added to Formula (4), with diameter D expressed in millimetres:
    if D_mm < 71.12:
        additional_term = 0.011*(0.75-beta)*(2.8-(D_mm/25.4))
    else:
        additional_term = 0.0

    C = 0.5961 + 0.0261*beta**2 - 0.216*beta**8 + 0.000521 * (1e6*beta/Re)**0.7 + (0.0188 + 0.0063*A)*beta**3.5*(1e6/Re)**0.3 \
        + (0.043 + 0.080*e**(-10*L1) - 0.123*e**(-7*L1)) * (1-0.11*A)*(beta**4/(1-beta**4)) \
        - 0.031*(M2-0.8*M2**1.1)*beta**1.3 + additional_term

    return C


def _gas_densiometric_Froude_number(massflow_gas, D, rho_g, rho_l):
    """
    Calculate the gas densiometric Froude number (Frg) for wet-gas flow in a venturi.

    Parameters
    ----------
    massflow_gas : float
        Gas mass flow rate [kg/s]
    D : float
        Upstream inner pipe diameter [m]
    rho_g : float
        Gas density [kg/m3]
    rho_l : float
        Liquid density [kg/m3]
    
    Returns
    -------
    Frg : float
        Gas densiometric Froude number (Frg) [-]
    """

    if D <= 0.0 or rho_g <= 0.0 or rho_l <= 0.0 or massflow_gas < 0.0 or (rho_l - rho_g) == 0.0:
        return np.nan

    Fr_gas = (4*massflow_gas/(rho_g*pi*D**2*sqrt(9.81*D))) * sqrt(rho_g/(rho_l - rho_g))

    return Fr_gas


def calculate_C_wetgas_venturi_ReaderHarrisGraham(Fr_gas_th, X):
    """
    Calculate the discharge coefficient correction for wet-gas Venturi flow meters using the Reader-Harris/Graham correlation [1_].

    Parameters
    ----------
    Fr_gas_th : float
        Gas densiometric Froude number (Frg) [-]
    X : float
        Lockhart-Martinelli parameter [-]

    Returns
    -------
    C_wet : float
        Wet gas discharge coefficient [-]

    References
    ----------
    .. [1] Reader-Harris, M. and Graham, E. An improved model for venturi-tube overreading in wet gas, North Sea Flow Measurement Workshop, 2009.

    """

    if Fr_gas_th < 0.0 or X < 0.0:
        return np.nan

    C_wet = 1-0.0463*np.exp(-0.05*Fr_gas_th)*min(1,sqrt(X/0.016))

    return C_wet


def calculate_flow_wetgas_venturi_ReaderHarrisGraham(
    D, d, P1, dP, rho_g, rho_l, GMF=None, GVF=None, H=1, epsilon=None, kappa=None, check_input=False):
    """
    Calculate flowrates for a standard venturi meter in wet-gas conditions using the Reader-Harris/Graham correlation [1_], described in ISO/TR 11583:2012 [2_].
    
    The function uses an iterative approach to solve for the corrected gas mass flow rate. It calculates initial flow rates, 
    then iteratively updates the Lockhart-Martinelli parameter, Froude numbers, discharge coefficient, and over-read factor 
    until convergence is achieved.
    
    The function accepts either gas mass fraction (GMF) or gas volume fraction (GVF) as input. If both are provided, GMF is used.
    The function accepts either expansibility (epsilon) or isentropic exponent (kappa) as input. If both are provided, epsilon is used.

    H is a dimensionless parameter which is a function of the surface tension of the liquid. 
    H equals 1 for hydrocarbon liquids, 1.35 for water. 

    Valid for the following conditions:
    0.4 ≤ β ≤ 0.75 
    0 < X ≤ 0.3 
    3 < Fr_gas,th 
    0.02 < rho_g/rho_l
    D ≥ 50 mm 

    Parameters
    ----------
    D : float
        Pipe diameter [m]
    d : float
        Throat diameter [m]
    P1 : float
        Upstream pressure [bara]
    dP : float
        Differential pressure [mbar]
    rho_g : float
        Gas density [kg/m3]
    rho_l : float
        Liquid density [kg/m3]
    GMF : float, optional
        Gas mass fraction (by mass, 0 < GMF <= 1). Either GMF or GVF must be provided.
    GVF : float, optional
        Gas volume fraction (by volume, 0 < GVF <= 1). Either GMF or GVF must be provided.
    H : float, optional
        Dimensionless fluid parameter (default 1, which is used for hydrocarbon liquids, 1.35 for water)
    epsilon : float, optional
        Expansion factor. If not provided, calculated from kappa.
    kappa : float, optional
        Isentropic exponent (required if epsilon is not provided)
    check_input : bool, optional
        If True, checks input validity and raises exceptions for invalid inputs.
        If False, returns NaN results for invalid inputs.

    Returns
    -------
    results : dict
        Dictionary containing:
        - 'MassFlow_gas_initial': Initial uncorrected gas mass flow [kg/h]
        - 'MassFlow_gas_corrected': Final corrected gas mass flow [kg/h]
        - 'MassFlow_liq': Final liquid mass flow [kg/h]
        - 'MassFlow_tot': Final total mass flow [kg/h]
        - 'VolFlow_gas': Final gas volume flow [m3/h]
        - 'VolFlow_liq': Final liquid volume flow [m3/h]
        - 'VolFlow_tot': Final total volume flow [m3/h]
        - 'OverRead': Final over-read factor (OR) [-]
        - 'C_wet': Final wet-gas discharge coefficient [-]
        - 'LockhartMartinelli': Final Lockhart-Martinelli parameter X [-]
        - 'Fr_gas': Final gas densiometric Froude number [-]
        - 'Fr_gas_th': Final throat gas densiometric Froude number [-]
        - 'n': Final n parameter [-]
        - 'C_Ch': Final Chisholm coefficient [-]
        - 'epsilon': Expansion factor used [-]
        - 'iterations': Number of iterations to convergence [-]
        
        If inputs are invalid and check_input=False, all values will be NaN.

    Notes
    -----
    The iteration process continues until the relative change in corrected gas mass flow 
    is less than 1e-10 or until 100 iterations are reached. If convergence is not achieved
    and check_input=True, an exception is raised. If check_input=False, NaN results are returned.

    References
    ----------
    .. [1] Reader-Harris, M. and E. Graham, An improved model for Venturi-tube over reading in wet gas. North Sea Flow Measurement Workshop, 2009 
    .. [2] ISO/TR 11583:2012, Measurement of wet gas flow by means of pressure differential devices inserted in circular cross-section conduits.
    
    """
    # Define results dictionary with NaN values for consistent return structure
    results = {
        "MassFlow_gas_initial": np.nan,
        "MassFlow_gas_corrected": np.nan,
        "MassFlow_liq": np.nan,
        "MassFlow_tot": np.nan,
        "VolFlow_gas": np.nan,
        "VolFlow_liq": np.nan,
        "VolFlow_tot": np.nan,
        "OverRead": np.nan,
        "C_wet": np.nan,
        "LockhartMartinelli": np.nan,
        "Fr_gas": np.nan,
        "Fr_gas_th": np.nan,
        "n": np.nan,
        "C_Ch": np.nan,
        "epsilon": np.nan,
        "iterations": np.nan,
    }

    # Input validation and GMF/GVF handling
    if check_input:
        if D <= 0.0:
            raise Exception("Pipe diameter D must be greater than zero.")
        if d <= 0.0:
            raise Exception("Throat diameter d must be greater than zero.")
        if d >= D:
            raise Exception("Throat diameter d must be smaller than pipe diameter D.")
        if P1 <= 0.0:
            raise Exception("Upstream pressure P1 must be greater than zero.")
        if dP < 0.0:
            raise Exception("Differential pressure dP must be non-negative.")
        if rho_g <= 0.0:
            raise Exception("Gas density rho_g must be greater than zero.")
        if rho_l <= 0.0:
            raise Exception("Liquid density rho_l must be greater than zero.")
        if GMF is None and GVF is None:
            raise Exception("Either GMF or GVF must be provided.")
        if GMF is not None and not (0 < GMF <= 1):
            raise Exception("GMF must be in the range (0, 1].")
        if GVF is not None and not (0 < GVF <= 1):
            raise Exception("GVF must be in the range (0, 1].")
    else:
        if D <= 0.0 or d <= 0.0 or d >= D or P1 <= 0.0 or dP < 0.0 or rho_g <= 0.0 or rho_l <= 0.0:
            return results
        if GMF is None and GVF is None:
            return results
        if GMF is not None and not (0 < GMF <= 1):
            return results
        if GVF is not None and not (0 < GVF <= 1):
            return results

    # Convert GVF to GMF if needed
    if GMF is None:
        GMF = _GVF_to_GMF(GVF=GVF, rho_gas=rho_g, rho_liquid=rho_l)

    beta = calculate_beta_DP_meter(D=D, d=d)

    # Calculate expansibility for gas
    if epsilon is None:
        epsilon_used = calculate_expansibility_venturi(
            P1=P1,
            dP=dP,
            beta=beta,
            kappa=kappa
        )
    else:
        epsilon_used = epsilon

    # Initial calculation of gas flowrates using gas density only
    venturi_results_gas = calculate_flow_venturi(
        D=D,
        d=d,
        dP=dP,
        rho1=rho_g,
        C=1.0,
        epsilon=epsilon_used,
        check_input=check_input
    )

    MassFlow_gas_initial = venturi_results_gas['MassFlow'] # kg/h
    MassFlow_liq_initial = (MassFlow_gas_initial*(1-GMF))/GMF # kg/h

    # Calculate Lockhart-Martinelli parameter
    X = _lockhart_martinelli_parameter(
        mass_flow_rate_liquid=MassFlow_liq_initial/3600, # Convert to kg/s
        mass_flow_rate_gas=MassFlow_gas_initial/3600, # Convert to kg/s
        density_liquid=rho_l,
        density_gas=rho_g
    )

    # Calculate gas densiometric Froude number
    Fr_gas = _gas_densiometric_Froude_number(
        massflow_gas=MassFlow_gas_initial/3600, # Convert to kg/s
        D=D,
        rho_g=rho_g,
        rho_l=rho_l
    )

    Fr_gas_th = Fr_gas / beta**2.5

    # Calculate wet-gas discharge coefficient
    C_wet = calculate_C_wetgas_venturi_ReaderHarrisGraham(
        Fr_gas_th=Fr_gas_th,
        X=X
    )

    # Calculate n
    n = max(0.583 - 0.18*beta**2 - 0.578*np.exp(-0.8*Fr_gas/H), 0.392 - 0.18*beta**2)

    # Calculate Chisholm coefficient
    C_Ch = (rho_l/rho_g)**n + (rho_g/rho_l)**n

    # Calculate over-read
    OR = sqrt(1 + C_Ch*X + X**2)

    # Calculate corrected gas mass flow using the over-read factor and wet-gas discharge coefficient
    MassFlow_gas_corrected = (MassFlow_gas_initial / OR) * C_wet

    # Iteration parameters
    max_iterations = 100
    tolerance = 1e-10 # Tolerance is set to match number of iterations provided in the ISO. 
    MassFlow_gas_corrected_new = MassFlow_gas_corrected
    
    for iteration in range(max_iterations):

        # Calculate gas densiometric Froude number
        Fr_gas = _gas_densiometric_Froude_number(
            massflow_gas=MassFlow_gas_corrected_new / 3600, # Convert to kg/s
            D=D,
            rho_g=rho_g,
            rho_l=rho_l
        )

        Fr_gas_th = Fr_gas / beta**2.5

        # Calculate wet-gas discharge coefficient
        C_wet = calculate_C_wetgas_venturi_ReaderHarrisGraham(
            Fr_gas_th=Fr_gas_th,
            X=X
        )

        # Calculate n
        n = max(0.583 - 0.18*beta**2 - 0.578*np.exp(-0.8*Fr_gas/H), 0.392 - 0.18*beta**2)

        # Calculate Chisholm coefficient
        C_Ch = (rho_l/rho_g)**n + (rho_g/rho_l)**n

        # Calculate over-read
        OR = sqrt(1 + C_Ch*X + X**2)

        # Calculate new corrected gas mass flow
        MassFlow_gas_corrected_new = (MassFlow_gas_initial / OR) * C_wet

        # Check for convergence
        relative_error = abs(MassFlow_gas_corrected_new - MassFlow_gas_corrected) / MassFlow_gas_corrected
        if relative_error < tolerance:
            MassFlow_gas_corrected = MassFlow_gas_corrected_new
            break
            
        MassFlow_gas_corrected = MassFlow_gas_corrected_new
    
    else:
        # If we reach here, iterations didn't converge
        if check_input:
            raise Exception(f"Wet-gas Venturi calculation did not converge after {max_iterations} iterations")
        else:
            return results

    # Final total and liquid mass flow calculation
    MassFlow_tot_final = MassFlow_gas_corrected / GMF
    MassFlow_liq_final = MassFlow_tot_final*(1-GMF)

    # Calculate volume flow
    VolFlow_gas = MassFlow_gas_corrected / rho_g # m3/h
    VolFlow_liq = MassFlow_liq_final / rho_l # m3/h
    VolFlow_tot = VolFlow_gas + VolFlow_liq # m3/h Assuming no volume change on mixing and homogeneous flow

    # Update results dictionary with calculated values
    results.update({
        "MassFlow_gas_initial": MassFlow_gas_initial,
        "MassFlow_gas_corrected": MassFlow_gas_corrected,
        "MassFlow_liq": MassFlow_liq_final,
        "MassFlow_tot": MassFlow_tot_final,
        "VolFlow_gas": VolFlow_gas,
        "VolFlow_liq": VolFlow_liq,
        "VolFlow_tot": VolFlow_tot,
        "OverRead": OR,
        "C_wet": C_wet,
        "LockhartMartinelli": X,
        "Fr_gas": Fr_gas,
        "Fr_gas_th": Fr_gas_th,
        "n": n,
        "C_Ch": C_Ch,
        "epsilon": epsilon_used,
        "iterations": iteration + 1,
    })

    return results


# Have not validated the homogeneous model yet, so commenting out for now

# def calculate_flow_venturi_homogeneous_wetgas(
#     D, d, dP, rho_g, rho_l, GMF, C=None, epsilon=None, check_input=False
# ):
#     """
#     Calculate the corrected gas mass flow rate for a Venturi meter in wet-gas conditions
#     using the homogeneous correction model.

#     NOTE: This function has not been validated yet. Use with caution.

#     Parameters
#     ----------
#     D : float
#         Pipe diameter [m]
#     d : float
#         Throat diameter [m]
#     dP : float
#         Differential pressure [mbar]
#     rho_g : float
#         Gas density [kg/m3]
#     rho_l : float
#         Liquid density [kg/m3]
#     GMF : float
#         Gas mass fraction (by mass, 0 < GMF <= 1)
#     C : float, optional
#         Discharge coefficient (default 0.984)
#     epsilon : float, optional
#         Expansion factor (default 1.0)
#     check_input : bool, optional
#         If True, checks input validity

#     Returns
#     -------
#     results : dict
#         Dictionary containing:
#         - 'MassFlow_indicated': Uncorrected gas mass flow [kg/h]
#         - 'MassFlow_corrected': Corrected gas mass flow [kg/h]
#         - 'OverRead': Over-read factor (OR)
#         - 'MixtureDensity': Homogeneous mixture density [kg/m3]
#         - 'LockhartMartinelli': Lockhart-Martinelli parameter X
#         - 'GMF': Gas mass fraction used
#         - 'C': Discharge coefficient used
#         - 'epsilon': Expansion factor used
#         - 'iterations': Number of iterations to convergence
#     """
#     # Input checks
#     if check_input:
#         if D <= 0.0 or d <= 0.0 or dP <= 0.0 or rho_g <= 0.0 or rho_l <= 0.0 or not (0 < GMF <= 1):
#             raise Exception("Invalid input parameters for wet-gas Venturi calculation.")

#     # Defaults
#     C_used = C if C is not None else 0.984
#     epsilon_used = epsilon if epsilon is not None else 1.0

#     # Step 1: Calculate initial gas mass flow using gas density only
#     venturi_results_gas = calculate_flow_venturi(
#         D=D,
#         d=d,
#         dP=dP,
#         rho1=rho_g,
#         C=C_used,
#         epsilon=epsilon_used,
#         check_input=check_input
#     )
    
#     MassFlow_gas_initial = venturi_results_gas['MassFlow']

#     # Iteration parameters
#     max_iterations = 100
#     tolerance = 1e-6
#     MassFlow_corrected = MassFlow_gas_initial
    
#     for iteration in range(max_iterations):
#         # Step 2: Calculate total mass flow from corrected gas mass flow
#         MassFlow_total = MassFlow_corrected / GMF
        
#         # Step 3: Calculate individual phase mass flow rates
#         mass_flow_rate_gas = MassFlow_corrected
#         mass_flow_rate_liquid = MassFlow_total - MassFlow_corrected
        
#         # Step 4: Calculate Lockhart-Martinelli parameter
#         X = _lockhart_martinelli_parameter(
#             mass_flow_rate_liquid=mass_flow_rate_liquid,
#             mass_flow_rate_gas=mass_flow_rate_gas,
#             density_liquid=rho_l,
#             density_gas=rho_g
#         )
        
#         # Step 5: Calculate homogeneous correction factor and over-read
#         C_hom = (rho_g / rho_l) ** 0.5 + (rho_l / rho_g) ** 0.5
#         OR = (1 + C_hom * X + X ** 2) ** 0.5
        
#         # Step 6: Calculate new corrected mass flow
#         MassFlow_corrected_new = MassFlow_gas_initial / OR
        
#         # Check for convergence
#         relative_error = abs(MassFlow_corrected_new - MassFlow_corrected) / MassFlow_corrected
#         if relative_error < tolerance:
#             MassFlow_corrected = MassFlow_corrected_new
#             break
            
#         MassFlow_corrected = MassFlow_corrected_new
    
#     else:
#         # If we reach here, iterations didn't converge
#         if check_input:
#             raise Exception(f"Wet-gas Venturi calculation did not converge after {max_iterations} iterations")
    
#     # Final calculations
#     MassFlow_total_final = MassFlow_corrected / GMF
#     mass_flow_rate_liquid_final = MassFlow_total_final - MassFlow_corrected
#     rho_hom = rho_l * (mass_flow_rate_liquid_final / MassFlow_total_final) + rho_g * (MassFlow_corrected / MassFlow_total_final)

#     results = {
#         "MassFlow_indicated": MassFlow_gas_initial,
#         "MassFlow_corrected": MassFlow_corrected,
#         "OverRead": OR,
#         "MixtureDensity": rho_hom,
#         "LockhartMartinelli": X,
#         "GMF": GMF,
#         "C": C_used,
#         "epsilon": epsilon_used,
#         "iterations": iteration + 1,
#     }
#     return results
