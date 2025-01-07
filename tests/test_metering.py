from pvtlib import metering, utilities
import os

#%% Test venturi calculations



#%% Test V-cone calculations
def test_V_cone_calculation_1():
    '''
    Validate V-cone calculation against data from V-cone Data Sheet   
    '''
    
    criteria = 0.003 # %
    
    beta = metering.calculate_beta_V_cone(D=0.073406, dc=0.0586486)
    
    dP = 603.29
    epsilon = 0.9809
    
    res = metering.calculate_flow_V_cone(
        D=0.073406,  
        beta=beta, 
        dP=dP,
        rho1=14.35,
        C = 0.8259,
        epsilon = epsilon
        )
    
    #Calculate relative deviation [%] in mass flow from reference
    reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'],(1.75*3600)))
    
    assert reldev<criteria, f'V-cone calculation failed for {dP} mbar dP'
    
    dP = 289.71
    epsilon = 0.9908
    
    res = metering.calculate_flow_V_cone(
        D=0.073406,
        beta=beta,
        dP=dP,
        rho1=14.35,
        C = 0.8259,
        epsilon = epsilon
        )
    
    #Calculate relative deviation [%] in mass flow from reference
    reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'],(1.225*3600)))
    
    assert reldev<criteria, f'V-cone calculation failed for {dP} mbar dP'
    
    dP = 5.8069
    epsilon = 0.9998
    
    res = metering.calculate_flow_V_cone(
        D=0.073406,
        beta=beta,
        dP=dP,
        rho1=14.35,
        C = 0.8259,
        epsilon = epsilon
        )
    
    #Calculate relative deviation [%] in mass flow from reference
    reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'],(0.175*3600)))
    
    assert reldev<criteria, f'V-cone calculation failed for {dP} mbar dP'
    

def test_V_cone_calculation_2():
    '''
    Validate V-cone calculation against data from datasheet
    '''
    
    criteria = 0.1 # [%] Calculations resulted in 0.05% deviation from the value in datasheet due to number of decimals
    
    dP = 71.66675
    epsilon = 0.9809
    
    res = metering.calculate_flow_V_cone(
        D=0.024,  
        beta=0.55, 
        dP=dP,
        rho1=0.362,
        C = 0.8389,
        epsilon = 0.99212
        )
    
    #Calculate relative deviation [%] in mass flow from reference
    reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'],31.00407))
    
    assert reldev<criteria, f'V-cone calculation failed for {dP} mbar dP'


def test_calculate_beta_V_cone():
    '''
    Validate calculate_beta_V_cone function against data from V-cone datasheet
    
    Meter tube diameter	24	mm
    Cone diameter dr	20.044	mm
    Cone beta ratio	0.55	
    
    '''
    
    criteria = 0.001 # %
    
    # Unit of inputs doesnt matter, as long as its the same for both D and dc. mm used in this example
    beta = metering.calculate_beta_V_cone(
        D=24, #mm
        dc=20.044 #mm
        )
    
    reldev = utilities.calculate_relative_deviation(beta,0.55)
    
    assert reldev<criteria, f'V-cone beta calculation failed'
    
    
def test_calculate_expansibility_Stewart_V_cone():
    '''
    Validate V-cone calculation against data from V-cone Data Sheet
    The code also validates the beta calculation
    
    dP = 484.93
    kappa = 1.299
    D=0.073406 (2.8900 in)
    dc=0.0586486 (2.3090 in)
    beta=0.6014
    '''
    
    beta = metering.calculate_beta_V_cone(D=0.073406, dc=0.0586486)
    
    criteria = 0.003 # %
    
    epsilon = metering.calculate_expansibility_Stewart_V_cone(
        beta=beta, 
        P1=18.0, 
        dP=484.93, 
        k=1.299
        )
    
    assert round(epsilon,4)==0.9847, 'Expansibility calculation failed'
    
    assert round(beta,4)==0.6014, 'Beta calculation failed'



#%% Test venturi calculations
# def test_calculate_flow_venturi():
#     '''
#     Validate Venturi calculation against known values.
#     '''
    
#     criteria = 0.1 # [%] Allowable deviation
    
#     # Test case 1
#     res = metering.calculate_flow_venturi(
#         D=0.1, 
#         d=0.05, 
#         dP=100, 
#         rho1=1000
#     )
    
#     expected_mass_flow = 500.0
#     reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'], expected_mass_flow))
#     assert reldev < criteria, f'Venturi calculation failed for test case 1'

def test_calculate_beta_venturi():
    assert metering.calculate_beta_venturi(D=0.1, d=0.05)==0.5, 'Beta calculation failed'
    assert metering.calculate_beta_venturi(D=0.2, d=0.05)==0.25, 'Beta calculation failed'


def test_calculate_expansibility_ventiruri():
    '''
    Validate calculate_expansibility_venturi function against known values from ISO 5176-4:2022, table A.1
    '''

    cases = {
        'case1': {
            'P1': 50,
            'dP': 12500,
            'kappa': 1.2,
            'beta': 0.75,
            'expected': 0.7690
        },
        'case2': {
            'P1': 50,
            'dP': 3000,
            'kappa': 1.4,
            'beta': 0.75,
            'expected': 0.9489
        },
        'case3': {
            'P1': 100,
            'dP': 2000,
            'kappa': 1.66,
            'beta': 0.3,
            'expected': 0.9908
        },
        'case4': {
            'P1': 100,
            'dP': 25000,
            'kappa': 1.4,
            'beta': 0.5623,
            'expected': 0.8402
        },
    }

    for case, case_dict in cases.items():
        epsilon = metering.calculate_expansibility_venturi(
            P1=case_dict['P1'],
            dP=case_dict['dP'],
            beta=case_dict['beta'],
            kappa=case_dict['kappa']
        )
        assert round(epsilon,4)==case_dict['expected'], f'Expansibility calculation failed for {case}'
