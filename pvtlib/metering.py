from math import sqrt, pi

#%% V-cone equations
def calculate_flow_V_cone(D, beta, dP, rho1, C = None, epsilon = None):
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
            - 8 × 104 ≤ ReD ≤ 1,2 × 107
    epsilon : float, optional
        expansibility factor (ε) is a coefficient used to take into account the compressibility of the fluid. 
        If no expansibility is provided, the function will use 1.0. 

    Returns
    -------
    results : dict
        A dictionary containing the following key-value pairs:
            'MassFlow': The mass flowrate of the fluid in kg/h.
            'VolFlow': The volume flowrate of the fluid in m3/h.
            'Velocity': The velocity of the fluid in m/s.
            'C': The discharge coefficient used in the calculations.
            'epsilon': The expansibility factor used in the calculations.
        
    '''
    
    # Dictionary containing all results from calculations
    results = {}
    
    if D<=0.0:
        raise Exception('ERROR: Negative diameter input. Diameter (D) must be a float greater than zero')
    
    if rho1<=0.0:
        raise Exception('ERROR: Negative density input. Density (rho1) must be a float greater than zero')
    
    if dP<0.0:
        raise Exception('ERROR: Negative dP input. dP must be a float greater than zero')
    
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


def calculate_expansibility_Stewart_V_cone(beta , P1, dP, k):
    '''Calculates the expansibility factor for a cone flow meter,
    based on the geometry of the cone meter, measured differential pressures of the orifice,
    and the isentropic exponent of the fluid. 

    .. math::
        \epsilon = 1 - (0.649 + 0.696\beta^4) \frac{\Delta P}{\kappa P_1}

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
    
    beta = sqrt(1-((dc**2)/(D**2)))
    
    return beta