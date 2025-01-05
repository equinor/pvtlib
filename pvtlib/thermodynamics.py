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