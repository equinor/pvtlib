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

from pvtlib.fluid_mechanics import reynolds_number, superficial_velocity

def _calculate_flow_DP_meter(C, D, d, epsilon, dP, rho1):
    """
    Calculate the mass flow rate through a differential pressure (DP) meter.
    This formula is given as "Formula (1)" in ISO 5167 part 2 and 4 (2022 edition),
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
    results['Velocity'] = superficial_velocity(results['VolFlow'], D) # m/s

    return results


#%% Venturi equations
def calculate_flow_venturi(D, d, dP, rho1, C=None, epsilon=None, check_input=False):
    '''
    Calculate the flow rate using a Venturi meter.
    Calculations performed according to ISO 5167-4:2022.

    If discharge coefficient is not provided, the function uses the value of 0.984 given in ISO 5167-4:2022, 
    which is valid for an "as cast" convergent section Classical Venturi tube at the following conditions:
        - 100 mm ≤ D ≤ 800 mm
        - 0.3 ≤ β ≤ 0.75
        - 2 × 10^5 ≤ ReD ≤ 2 × 10^6

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
    Calculate the expansibility factor for a Venturi meter.

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
    From ISO 5167-1:2022:
    In ISO 5167-2 and ISO 5167-3 the diameter ratio is the ratio of the diameter of the throat of the
    primary device to the internal diameter of the measuring pipe upstream of the primary device.
    In ISO 5167-4, where the primary device has a cylindrical section upstream, having the same
    diameter as that of the pipe, the diameter ratio is the ratio of the throat diameter to the diameter of this cylindrical
    section at the plane of the upstream pressure tappings.

    This function cannot be used for cone meters, as the diameter ratio is defined differently (see calculate_beta_V_cone).    '''
    
    if D<=0.0:
        raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')

    beta = d/D
    
    return beta



#%% V-cone equations
def calculate_flow_V_cone(D, beta, dP, rho1, C = None, epsilon = None, check_input=False):
    '''
    Calculate mass flowrate and volume flowrate of a V-cone meter. 
    Calculations performed according to NS-EN ISO 5167-5:2022. 

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
        Under the following conditions, the value of the discharge coefficient, C, for an uncalibrated meter is C=0.82
            - 50 mm ≤ D ≤ 500 mm
            - 0,45 ≤ β ≤ 0,75
            - 8 × 10^4 ≤ ReD ≤ 1,2 × 10^7
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
    based on the geometry of the cone meter, measured differential pressures of the orifice,
    and the isentropic exponent of the fluid. 

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
        Expansibility factor (1 for incompressible fluids, less than 1 for
        real fluids), [-]

    Notes
    -----
    This formula was determined for the range of P2/P1 >= 0.75; the only gas
    used to determine the formula is air.

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
    Calculates V-cone beta according to NS-EN ISO 5167-5:2022
    Figure 1 in NS-EN ISO 5167-5:2022 illustrates the locations of D and dc in the cone meter, and how beta changes with dc. 

    beta edge: maximum circumference of the cone

    Parameters
    ----------
    D : float
        The diameter of the pipe at the beta edge, D. 
        Assumes that the diameter of the pipe at the upstream tapping, DTAP, is equal to the diameter of the pipe at the beta edge, D. 
        In easier terms, its the inlet diameter. 
        
    dc : float
        dc is the diameter of the cone in the plane of the beta edge [m]. 
        In easier terms, its the diameter of the cone. 

    Returns
    -------
    beta : float
        V-cone beta.

    '''
    
    if D<=0.0:
        raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')

    beta = sqrt(1-((dc**2)/(D**2)))
    
    return beta


#%% Orifice equations
def calculate_flow_orifice(D, d, dP, rho1, mu=None, C=None, epsilon=None, tapping='corner', check_input=False):
    """
    Calculate the flow rate through an orifice plate.
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
        results['Re'] = reynolds_number(rho=rho1, v=results['Velocity'], D=D, mu=mu)
        
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
            Re = reynolds_number(rho=rho1, v=results['Velocity'], D=D, mu=mu)

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
    Calculate the expansibility factor for an orifice meter according to ISO 5167-2:2022 (formula 5). 
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
    Calculate the discharge coefficient (C) for an orifice plate using the Reader-Harris/Gallagher equation.
    Perform calculations according to ISO 5167-2:2022.
    
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
