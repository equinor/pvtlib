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

from pvtlib import utilities
import numpy as np

from pvtlib.metering import differential_pressure_flowmeters

#%% Test V-cone calculations
def test_V_cone_calculation_1():
    '''
    Validate V-cone calculation against data from V-cone Data Sheet   
    '''
    
    criteria = 0.003 # %
    
    beta = differential_pressure_flowmeters.calculate_beta_V_cone(D=0.073406, dc=0.0586486)
    
    dP = 603.29
    epsilon = 0.9809
    
    res = differential_pressure_flowmeters.calculate_flow_V_cone(
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
    
    res = differential_pressure_flowmeters.calculate_flow_V_cone(
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
    
    res = differential_pressure_flowmeters.calculate_flow_V_cone(
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
    
    res = differential_pressure_flowmeters.calculate_flow_V_cone(
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
    beta = differential_pressure_flowmeters.calculate_beta_V_cone(
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
    
    beta = differential_pressure_flowmeters.calculate_beta_V_cone(D=0.073406, dc=0.0586486)
    
    criteria = 0.003 # %
    
    epsilon = differential_pressure_flowmeters.calculate_expansibility_Stewart_V_cone(
        beta=beta, 
        P1=18.0, 
        dP=484.93, 
        k=1.299
        )
    
    assert round(epsilon,4)==0.9847, 'Expansibility calculation failed'
    
    assert round(beta,4)==0.6014, 'Beta calculation failed'


#%% Test venturi calculations
def test_calculate_flow_venturi():
    '''
    Validate Venturi calculation against known values.
    '''

    # Cases generated based on the python fluids package (fluids==1.1.0)
    cases = {
        'case1': {'D': 0.13178, 'd': 0.06664, 'dP': 200, 'rho': 39.6, 'C': 0.984, 'epsilon': 0.997456, 'expected_massflow': 16044.073835047437, 'expected_volflow': 405.1533796729151},
        'case2': {'D': 0.13178, 'd': 0.06664, 'dP': 800, 'rho': 39.6, 'C': 0.984, 'epsilon': 0.997456, 'expected_massflow': 32088.147670094873, 'expected_volflow': 810.3067593458302},
        'case3': {'D': 0.2, 'd': 0.15, 'dP': 800, 'rho': 39.6, 'C': 0.984, 'epsilon': 0.997456, 'expected_massflow': 190095.69790414887, 'expected_volflow': 4800.396411720931},
        'case4': {'D': 0.2, 'd': 0.15, 'dP': 800, 'rho': 20.0, 'C': 0.984, 'epsilon': 0.997456, 'expected_massflow': 135095.12989761416, 'expected_volflow': 6754.756494880708},
        'case5': {'D': 0.2, 'd': 0.15, 'dP': 800, 'rho': 39.6, 'C': 0.984, 'epsilon': 0.9, 'expected_massflow': 171522.48130617687, 'expected_volflow': 4331.375790560021}
    }

    criteria = 0.0001 # [%] Allowable deviation
    
    for case, case_dict in cases.items():
        res = differential_pressure_flowmeters.calculate_flow_venturi(
            D=case_dict['D'],
            d=case_dict['d'],
            dP=case_dict['dP'],
            rho1=case_dict['rho'],
            C=case_dict['C'],
            epsilon=case_dict['epsilon']
        )
        
        # Calculate relative deviation [%] in mass flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'], case_dict['expected_massflow']))
        
        assert reldev < criteria, f'Mass flow from venturi calculation failed for {case}'

        # Calculate relative deviation [%] in volume flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['VolFlow'], case_dict['expected_volflow']))
        
        assert reldev < criteria, f'Volume flow from venturi calculation failed for {case}'


def test_calculate_beta_DP_meter():
    assert differential_pressure_flowmeters.calculate_beta_DP_meter(D=0.1, d=0.05)==0.5, 'Beta calculation failed'
    assert differential_pressure_flowmeters.calculate_beta_DP_meter(D=0.2, d=0.05)==0.25, 'Beta calculation failed'


def test_calculate_expansibility_ventiruri():
    '''
    Validate calculate_expansibility_venturi function against known values from ISO 5176-4:2022, table A.1
    '''

    cases = {
        'case1': {'P1': 50, 'dP': 12500, 'kappa': 1.2, 'beta': 0.75, 'expected': 0.7690},
        'case2': {'P1': 50, 'dP': 3000, 'kappa': 1.4, 'beta': 0.75, 'expected': 0.9489},
        'case3': {'P1': 100, 'dP': 2000, 'kappa': 1.66, 'beta': 0.3, 'expected': 0.9908},
        'case4': {'P1': 100, 'dP': 25000, 'kappa': 1.4, 'beta': 0.5623, 'expected': 0.8402}
    }

    for case, case_dict in cases.items():
        epsilon = differential_pressure_flowmeters.calculate_expansibility_venturi(
            P1=case_dict['P1'],
            dP=case_dict['dP'],
            beta=case_dict['beta'],
            kappa=case_dict['kappa']
        )
        assert round(epsilon,4)==case_dict['expected'], f'Expansibility calculation failed for {case}'

#%% Test orifice calculations
def test_calculate_expansibility_orifice():
    '''
    Validate calculate_expansibility_orifice function against known values from ISO 5176-2:2022, table A.12
    '''
    cases = {
        'case1': {'P1': 50, 'dP': 12500, 'beta': 0.1, 'kappa': 1.2, 'expected': 0.9252},
        'case2': {'P1': 50, 'dP': 12500, 'beta': 0.75, 'kappa': 1.2, 'expected': 0.8881},
        'case3': {'P1': 50, 'dP': 1000, 'beta': 0.1, 'kappa': 1.2, 'expected': 0.9941},
        'case4': {'P1': 50, 'dP': 1000, 'beta': 0.75, 'kappa': 1.2, 'expected': 0.9912}
    }

    for case, case_dict in cases.items():
        epsilon = differential_pressure_flowmeters.calculate_expansibility_orifice(
            P1=case_dict['P1'],
            dP=case_dict['dP'],
            beta=case_dict['beta'],
            kappa=case_dict['kappa']
        )
        assert round(epsilon, 4) == case_dict['expected'], f'Expansibility calculation failed for {case}'


def test_calculate_C_orifice_ReaderHarrisGallagher():
    '''
    Validate calculate_C_orifice_ReaderHarrisGallagher function against known values.
    '''
    cases = {
        'case1': {'D': 0.1, 'beta': 0.1, 'Re': 5000, 'tapping': 'corner', 'expected': 0.6006},
        'case2': {'D': 0.1, 'beta': 0.1, 'Re': 100000000, 'tapping': 'corner', 'expected': 0.5964},
        'case3': {'D': 0.1, 'beta': 0.5, 'Re': 5000, 'tapping': 'corner', 'expected': 0.6276},
        'case4': {'D': 0.1, 'beta': 0.5, 'Re': 100000000, 'tapping': 'corner', 'expected': 0.6022},
        'case5': {'D': 0.072, 'beta': 0.1, 'Re': 5000, 'tapping': 'D', 'expected': 0.6003},
        'case6': {'D': 0.072, 'beta': 0.1, 'Re': 100000000, 'tapping': 'D', 'expected': 0.5961},
        'case7': {'D': 0.072, 'beta': 0.5, 'Re': 5000, 'tapping': 'D', 'expected': 0.6264},
        'case8': {'D': 0.072, 'beta': 0.5, 'Re': 100000000, 'tapping': 'D', 'expected': 0.6016},
        'case9': {'D': 0.05, 'beta': 0.25, 'Re': 5000, 'tapping': 'flange', 'expected': 0.6102},
        'case10': {'D': 0.05, 'beta': 0.25, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.6013},
        'case11': {'D': 0.05, 'beta': 0.75, 'Re': 5000, 'tapping': 'flange', 'expected': 0.6732},
        'case12': {'D': 0.05, 'beta': 0.75, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.6025},
        'case13': {'D': 0.075, 'beta': 0.17, 'Re': 10000, 'tapping': 'flange', 'expected': 0.6003},
        'case14': {'D': 0.075, 'beta': 0.17, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.5964},
        'case15': {'D': 0.075, 'beta': 0.75, 'Re': 10000, 'tapping': 'flange', 'expected': 0.6462},
        'case16': {'D': 0.075, 'beta': 0.75, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.6000},
        'case17': {'D': 1, 'beta': 0.1, 'Re': 100000, 'tapping': 'flange', 'expected': 0.5969},
        'case18': {'D': 1, 'beta': 0.1, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.5963},
        'case19': {'D': 1, 'beta': 0.75, 'Re': 100000, 'tapping': 'flange', 'expected': 0.6055},
        'case20': {'D': 1, 'beta': 0.75, 'Re': 100000000, 'tapping': 'flange', 'expected': 0.5905},
        'case21': {'D': 0.072, 'beta': 0.1, 'Re': 5000, 'tapping': 'D/2', 'expected': 0.6003},
        'case22': {'D': 0.072, 'beta': 0.1, 'Re': 100000000, 'tapping': 'D/2', 'expected': 0.5961},
        'case23': {'D': 0.072, 'beta': 0.5, 'Re': 5000, 'tapping': 'D/2', 'expected': 0.6264},
        'case24': {'D': 0.072, 'beta': 0.5, 'Re': 100000000, 'tapping': 'D/2', 'expected': 0.6016}
    }

    for case, case_dict in cases.items():
        C = differential_pressure_flowmeters.calculate_C_orifice_ReaderHarrisGallagher(
            D=case_dict['D'],
            beta=case_dict['beta'],
            Re=case_dict['Re'],
            tapping=case_dict['tapping']
        )
        
        assert round(C,4)==case_dict['expected'], f'C calculation failed for {case}'


def test_calculate_flow_orifice():

    # Cases generated based on the python fluids package (fluids==1.1.0)
    cases = {
        'case1': {'D': 0.3, 'd': 0.17, 'dP': 600, 'rho1': 20, 'mu': 0.0001, 'C': 0.65, 'epsilon': 0.99, 'massflow_per_hour': 86015.23377060085, 'volflow_per_hour': 4300.761688530043},
        'case2': {'D': 0.3, 'd': 0.17, 'dP': 400, 'rho1': 20, 'mu': 0.0001, 'C': 0.65, 'epsilon': 0.99, 'massflow_per_hour': 70231.14428139466, 'volflow_per_hour': 3511.557214069733},
        'case3': {'D': 0.3, 'd': 0.17, 'dP': 200, 'rho1': 20, 'mu': 0.0001, 'C': 0.65, 'epsilon': 0.99, 'massflow_per_hour': 49660.91837186499, 'volflow_per_hour': 2483.0459185932496},
        'case4': {'D': 0.3, 'd': 0.17, 'dP': 50, 'rho1': 20, 'mu': 0.0001, 'C': 0.65, 'epsilon': 0.99, 'massflow_per_hour': 24830.459185932494, 'volflow_per_hour': 1241.5229592966248},
        'case5': {'D': 0.2, 'd': 0.1, 'dP': 100, 'rho1': 20, 'mu': 0.0001, 'C': 0.55, 'epsilon': 0.99, 'massflow_per_hour': 10056.216708333148, 'volflow_per_hour': 502.81083541665737},
        'case6': {'D': 0.2, 'd': 0.1, 'dP': 75, 'rho1': 20, 'mu': 0.0001, 'C': 0.55, 'epsilon': 0.99, 'massflow_per_hour': 8708.939135378032, 'volflow_per_hour': 435.4469567689016},
        'case7': {'D': 0.2, 'd': 0.1, 'dP': 50, 'rho1': 20, 'mu': 0.0001, 'C': 0.55, 'epsilon': 0.99, 'massflow_per_hour': 7110.819027543829, 'volflow_per_hour': 355.54095137719145},
        'case8': {'D': 0.2, 'd': 0.1, 'dP': 25, 'rho1': 20, 'mu': 0.0001, 'C': 0.55, 'epsilon': 0.99, 'massflow_per_hour': 5028.108354166574, 'volflow_per_hour': 251.40541770832868},
        'case9': {'D': 1.0, 'd': 0.55, 'dP': 100, 'rho1': 50, 'mu': 0.00015, 'C': 0.6, 'epsilon': 0.98, 'massflow_per_hour': 527635.6305884372, 'volflow_per_hour': 10552.712611768744},
        'case10': {'D': 1.0, 'd': 0.55, 'dP': 1500, 'rho1': 50, 'mu': 0.00015, 'C': 0.6, 'epsilon': 0.98, 'massflow_per_hour': 2043524.0101346665, 'volflow_per_hour': 40870.48020269333},
        'case11': {'D': 0.05, 'd': 0.025, 'dP': 100, 'rho1': 50, 'mu': 0.00015, 'C': 0.6, 'epsilon': 0.98, 'massflow_per_hour': 1073.1590376626177, 'volflow_per_hour': 21.463180753252356},
        'case12': {'D': 0.05, 'd': 0.025, 'dP': 50, 'rho1': 50, 'mu': 0.00015, 'C': 0.6, 'epsilon': 0.98, 'massflow_per_hour': 758.8380328228665, 'volflow_per_hour': 15.17676065645733}
    }

    criteria = 0.0001 # [%] Allowable deviation

    for case, case_dict in cases.items():
        res = differential_pressure_flowmeters.calculate_flow_orifice(
            D=case_dict['D'],
            d=case_dict['d'],
            dP=case_dict['dP'],
            rho1=case_dict['rho1'],
            mu=case_dict['mu'],
            C=case_dict['C'],
            epsilon=case_dict['epsilon']
        )
        
        # Calculate relative deviation [%] in mass flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'], case_dict['massflow_per_hour']))
        
        assert reldev < criteria, f'Mass flow from orifice calculation failed for {case}'

        # Calculate relative deviation [%] in volume flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['VolFlow'], case_dict['volflow_per_hour']))
        
        assert reldev < criteria, f'Volume flow from orifice calculation failed for {case}'

def test_calculate_flow_orifice_without_C():
    # Test orifice calculation without a provided C value (will be calculated using Reader-Harris-Gallagher in an iterative process)

    # Cases generated based on the python fluids package (fluids==1.1.0)
    cases = {
        'case1': {'D': 0.3, 'd': 0.17, 'dP': 600, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'corner', 'massflow_per_hour': 80085.91838755546, 'volflow_per_hour': 4004.295919377773, 'C_calculated': 0.6051933438993131},
        'case2': {'D': 0.3, 'd': 0.17, 'dP': 400, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'corner', 'massflow_per_hour': 65414.248342171566, 'volflow_per_hour': 3270.7124171085784, 'C_calculated': 0.6054188901158989},
        'case3': {'D': 0.3, 'd': 0.17, 'dP': 200, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'flange', 'massflow_per_hour': 46249.23494614883, 'volflow_per_hour': 2312.4617473074413, 'C_calculated': 0.6053452835867839},
        'case4': {'D': 0.3, 'd': 0.17, 'dP': 50, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'flange', 'massflow_per_hour': 23166.34881177747, 'volflow_per_hour': 1158.3174405888735, 'C_calculated': 0.6064377068059384},
        'case5': {'D': 0.2, 'd': 0.1, 'dP': 100, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'D', 'massflow_per_hour': 11060.187865887872, 'volflow_per_hour': 553.0093932943936, 'C_calculated': 0.6049097292421641},
        'case6': {'D': 0.2, 'd': 0.1, 'dP': 75, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'D', 'massflow_per_hour': 9582.137318691242, 'volflow_per_hour': 479.1068659345621, 'C_calculated': 0.6051455227045194},
        'case7': {'D': 0.2, 'd': 0.1, 'dP': 50, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'D/2', 'massflow_per_hour': 7828.486950173011, 'volflow_per_hour': 391.42434750865056, 'C_calculated': 0.6055094083982603},
        'case8': {'D': 0.2, 'd': 0.1, 'dP': 25, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'D/2', 'massflow_per_hour': 5542.170314224395, 'volflow_per_hour': 277.10851571121975, 'C_calculated': 0.6062307050916101},
        'case9': {'D': 1.0, 'd': 0.55, 'dP': 100, 'rho1': 50, 'mu': 0.00015, 'epsilon': 0.98, 'tapping': 'flange', 'massflow_per_hour': 531416.2969186406, 'volflow_per_hour': 10628.325938372813, 'C_calculated': 0.6042991785744116},
        'case10': {'D': 1.0, 'd': 0.55, 'dP': 1500, 'rho1': 50, 'mu': 0.00015, 'epsilon': 0.98, 'tapping': 'corner', 'massflow_per_hour': 2056290.2561173881, 'volflow_per_hour': 41125.80512234776, 'C_calculated': 0.6037483032015505},
        'case11': {'D': 0.05, 'd': 0.025, 'dP': 100, 'rho1': 50, 'mu': 0.00015, 'epsilon': 0.98, 'tapping': 'D', 'massflow_per_hour': 1091.584843780707, 'volflow_per_hour': 21.83169687561414, 'C_calculated': 0.6103018129493022},
        'case12': {'D': 0.05, 'd': 0.025, 'dP': 50, 'rho1': 50, 'mu': 0.00015, 'epsilon': 0.98, 'tapping': 'D/2', 'massflow_per_hour': 773.4784497907841, 'volflow_per_hour': 15.469568995815683, 'C_calculated': 0.6115759223981871}
    }

    criteria = 0.0001 # [%] Allowable deviation

    for case, case_dict in cases.items():
        # Calculate orifice beta
        beta = differential_pressure_flowmeters.calculate_beta_DP_meter(D=case_dict['D'], d=case_dict['d'])

        res = differential_pressure_flowmeters.calculate_flow_orifice(
            D=case_dict['D'],
            d=case_dict['d'],
            dP=case_dict['dP'],
            rho1=case_dict['rho1'],
            mu=case_dict['mu'],
            epsilon=case_dict['epsilon'],
            tapping=case_dict['tapping']
        )

        # Calculate relative deviation [%] in mass flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'], case_dict['massflow_per_hour']))
        assert reldev < criteria, f'Mass flow from orifice calculation failed for {case}'

        # Calculate relative deviation [%] in discharge coefficient from reference
        reldev = abs(utilities.calculate_relative_deviation(res['C'], case_dict['C_calculated']))
        assert reldev < criteria, f'C from orifice calculation failed for {case}'

        # Calculate relative deviation [%] in volume flow from reference
        reldev = abs(utilities.calculate_relative_deviation(res['VolFlow'], case_dict['volflow_per_hour']))

        assert reldev < criteria, f'Volume flow from orifice calculation failed for {case}'


def test_calculate_flow_orifice_vs_ISO5167_1_E1():
    # Test orifice calculation against ISO 5167-1:2022, Annex E, E.1 Meter setup

    data={
        'D': 0.19368, # m
        'd': 0.09684, # m
        'dP': 257.6, # mbar
        'rho1': 13.93,
        'mu': 1.1145e-05,
        'C': 0.6026,
        'kappa': 1.308,
        'VolFlow': 1000.0,
        'MassFlow': 13928.4,
        'Re': 2282000.0,
        'Velocity': 9.43,
        'P1': 20.0, # bar
    }

    # Calculate orifice beta
    beta = differential_pressure_flowmeters.calculate_beta_DP_meter(D=data['D'], d=data['d'])

    # Calculate expansibility
    epsilon = differential_pressure_flowmeters.calculate_expansibility_orifice(
        P1=data['P1'],
        dP=data['dP'],
        beta=beta,
        kappa=data['kappa']
    )

    # Calculate discharge coefficient
    C = differential_pressure_flowmeters.calculate_C_orifice_ReaderHarrisGallagher(
        D=data['D'],
        beta=beta,
        Re=data['Re'],
        tapping='flange'
    )
    
    assert round(C, 4) == data['C'], 'Discharge coefficient calculation failed'

    # Calculate orifice flow, without any C provided
    res = differential_pressure_flowmeters.calculate_flow_orifice(
        D=data['D'],
        d=data['d'],
        dP=data['dP'],
        rho1=data['rho1'],
        mu=data['mu'],
        epsilon=epsilon,
        tapping='flange'
    )

    # Check that calculated C is equal to the actual C
    assert round(res['C'], 4) == data['C'], 'Discharge coefficient calculation failed'

    criteria = 0.02 # [%] Allowable deviation

    # Check that calculated mass flow, volume flow and velocity are within the criteria
    reldev = abs(utilities.calculate_relative_deviation(res['MassFlow'], data['MassFlow']))
    assert reldev < criteria, 'Mass flow from orifice calculation failed'

    reldev = abs(utilities.calculate_relative_deviation(res['VolFlow'], data['VolFlow']))
    assert reldev < criteria, 'Volume flow from orifice calculation failed'

    reldev = abs(utilities.calculate_relative_deviation(res['Velocity'], data['Velocity']))
    assert reldev < criteria, 'Velocity from orifice calculation failed'


def test_calculate_flow_orifice_invalid_inputs():
    # Test orifice calculation with invalid inputs. Should return np.nan for all cases
    cases = {
        'case1': {'D': -0.3, 'd': 0.17, 'dP': 600, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'corner'},
        'case2': {'D': 0.3, 'd': -0.17, 'dP': 600, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 5.0},
        'case3': {'D': 0.3, 'd': 0.17, 'dP': -600, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'corner'},
        'case4': {'D': 0.3, 'd': 0.17, 'dP': 600, 'rho1': -20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'corner'},
        'case5': {'D': 0.3, 'd': 0.17, 'dP': 600, 'rho1': 20, 'mu': None, 'epsilon': 0.99, 'tapping': 'corner'},
        'case6': {'D': 0.3, 'd': 0.17, 'dP': 600, 'rho1': 20, 'mu': 0.0001, 'epsilon': 0.99, 'tapping': 'invalid_tapping'}
    }

    for case_name, case_dict in cases.items():
        res = differential_pressure_flowmeters.calculate_flow_orifice(
            D=case_dict['D'],
            d=case_dict['d'],
            dP=case_dict['dP'],
            rho1=case_dict['rho1'],
            mu=case_dict['mu'],
            epsilon=case_dict['epsilon'],
            tapping=case_dict['tapping'],
            check_input=False
        )

        # Check that all results are np.nan
        for key in ['MassFlow', 'VolFlow', 'Velocity', 'C', 'epsilon', 'Re']:
            assert np.isnan(res[key])==True, f'Expected np.nan for {key} but got {res[key]} for case {case_name}'