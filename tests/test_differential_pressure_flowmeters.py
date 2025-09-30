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
    The function has been tested on a number of known cases. 
    Then these test cases have been generated, to cover a wider range of possible inputs.
    '''

    cases = {
        'case1': {'input': {'P1': 35, 'dP': 100, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.9980467431357704},
        'case2': {'input': {'P1': 35, 'dP': 100, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9987356572605486},
        'case3': {'input': {'P1': 35, 'dP': 100, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.997878316785603},
        'case4': {'input': {'P1': 35, 'dP': 100, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9986264901291529},
        'case5': {'input': {'P1': 35, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9962593507647453},
        'case6': {'input': {'P1': 35, 'dP': 100, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.99757614836258},
        'case7': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.899614076737725},
        'case8': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9337453194138332},
        'case9': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.8925476547341207},
        'case10': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9287487873782366},
        'case11': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.8320082913675725},
        'case12': {'input': {'P1': 35, 'dP': 5000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.8843729853868121},
        'case13': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.2457550899567365},
        'case14': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.39754696667366896},
        'case15': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.2383530278101653},
        'case16': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.3864259394370444},
        'case17': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.1901141720582873},
        'case18': {'input': {'P1': 35, 'dP': 30000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.3122336962440261},
        'case19': {'input': {'P1': 60, 'dP': 100, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.9988608537070035},
        'case20': {'input': {'P1': 60, 'dP': 100, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9992627453151632},
        'case21': {'input': {'P1': 60, 'dP': 100, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.9987624661940732},
        'case22': {'input': {'P1': 60, 'dP': 100, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9991990196822598},
        'case23': {'input': {'P1': 60, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9978156766058164},
        'case24': {'input': {'P1': 60, 'dP': 100, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.9985854442184993},
        'case25': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.9421417043773223},
        'case26': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9621390386244086},
        'case27': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.9376897372246114},
        'case28': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9591083318071002},
        'case29': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.8977845030559601},
        'case30': {'input': {'P1': 60, 'dP': 5000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.931294133721003},
        'case31': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.616892178020612},
        'case32': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.7301388847552639},
        'case33': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.6030137575054959},
        'case34': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.7172560230773798},
        'case35': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.5044791320574509},
        'case36': {'input': {'P1': 60, 'dP': 30000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.6202818596436332},
        'case37': {'input': {'P1': 100, 'dP': 100, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.9993165973477689},
        'case38': {'input': {'P1': 100, 'dP': 100, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9995577407004924},
        'case39': {'input': {'P1': 100, 'dP': 100, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.9992575181802543},
        'case40': {'input': {'P1': 100, 'dP': 100, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9995194902698783},
        'case41': {'input': {'P1': 100, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9986886385188124},
        'case42': {'input': {'P1': 100, 'dP': 100, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.999151050281699},
        'case43': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.9655104022448356},
        'case44': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.9775343631209875},
        'case45': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.9627260214778817},
        'case46': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.9756775519117771},
        'case47': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9370689604862881},
        'case48': {'input': {'P1': 100, 'dP': 5000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.9583073389128812},
        'case49': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.2, 'kappa': 1.1}, 'output': 0.7817695220879819},
        'case50': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.2, 'kappa': 1.7}, 'output': 0.8522891928883383},
        'case51': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.5, 'kappa': 1.1}, 'output': 0.7699181703051371},
        'case52': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.5, 'kappa': 1.7}, 'output': 0.8429482492407487},
        'case53': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.677872996111376},
        'case54': {'input': {'P1': 100, 'dP': 30000, 'beta': 0.8, 'kappa': 1.7}, 'output': 0.7662823502717088},
        }

    for case, case_dict in cases.items():
        epsilon = differential_pressure_flowmeters.calculate_expansibility_venturi(
            P1=case_dict['input']['P1'],
            dP=case_dict['input']['dP'],
            beta=case_dict['input']['beta'],
            kappa=case_dict['input']['kappa']
        )

        rel_dev = utilities.calculate_relative_deviation(epsilon, case_dict['output'])

        assert rel_dev < 0.000001, f'Expansibility calculation failed for {case}'
        

#%% Test orifice calculations
def test_calculate_expansibility_orifice():
    '''
    The function has been tested on a number of known cases. 
    Then these test cases have been generated, to cover a wider range of possible inputs.
    '''
    cases = {
        'case1': {'input': {'P1': 20, 'dP': 100, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9984040657578193},
        'case2': {'input': {'P1': 20, 'dP': 100, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9987454397117774},
        'case3': {'input': {'P1': 20, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9972180680579906},
        'case4': {'input': {'P1': 20, 'dP': 100, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9978131296097676},
        'case5': {'input': {'P1': 20, 'dP': 3000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9517871627245567},
        'case6': {'input': {'P1': 20, 'dP': 3000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9615274461268208},
        'case7': {'input': {'P1': 20, 'dP': 3000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9159584220411359},
        'case8': {'input': {'P1': 20, 'dP': 3000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9329370699107097},
        'case9': {'input': {'P1': 20, 'dP': 14000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.7664626550316556},
        'case10': {'input': {'P1': 20, 'dP': 14000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.7975180039814262},
        'case11': {'input': {'P1': 20, 'dP': 14000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.5929124255572498},
        'case12': {'input': {'P1': 20, 'dP': 14000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.6470461517034853},
        'case13': {'input': {'P1': 60, 'dP': 100, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9994681026995755},
        'case14': {'input': {'P1': 60, 'dP': 100, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9995820128016891},
        'case15': {'input': {'P1': 60, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9990728301637933},
        'case16': {'input': {'P1': 60, 'dP': 100, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.999271391071387},
        'case17': {'input': {'P1': 60, 'dP': 3000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9840073503994683},
        'case18': {'input': {'P1': 60, 'dP': 3000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.987371848182185},
        'case19': {'input': {'P1': 60, 'dP': 3000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9721226216060829},
        'case20': {'input': {'P1': 60, 'dP': 3000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9779874019981433},
        'case21': {'input': {'P1': 60, 'dP': 14000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9246737100688646},
        'case22': {'input': {'P1': 60, 'dP': 14000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9393197783617834},
        'case23': {'input': {'P1': 60, 'dP': 14000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.8686959609650706},
        'case24': {'input': {'P1': 60, 'dP': 14000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.8942260637299853},
        'case25': {'input': {'P1': 100, 'dP': 100, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9996808712992595},
        'case26': {'input': {'P1': 100, 'dP': 100, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9997492315876291},
        'case27': {'input': {'P1': 100, 'dP': 100, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9994437149709947},
        'case28': {'input': {'P1': 100, 'dP': 100, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9995628763153372},
        'case29': {'input': {'P1': 100, 'dP': 3000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.9904133749301968},
        'case30': {'input': {'P1': 100, 'dP': 3000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9924453638873472},
        'case31': {'input': {'P1': 100, 'dP': 3000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9832891996469033},
        'case32': {'input': {'P1': 100, 'dP': 3000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9868312346733482},
        'case33': {'input': {'P1': 100, 'dP': 14000, 'beta': 0.1, 'kappa': 1.1}, 'output': 0.955024077468818},
        'case34': {'input': {'P1': 100, 'dP': 14000, 'beta': 0.1, 'kappa': 1.4}, 'output': 0.9641495502198686},
        'case35': {'input': {'P1': 100, 'dP': 14000, 'beta': 0.8, 'kappa': 1.1}, 'output': 0.9216008077250957},
        'case36': {'input': {'P1': 100, 'dP': 14000, 'beta': 0.8, 'kappa': 1.4}, 'output': 0.9375077564333294},
        }

    for case, case_dict in cases.items():
        epsilon = differential_pressure_flowmeters.calculate_expansibility_orifice(
            P1=case_dict['input']['P1'],
            dP=case_dict['input']['dP'],
            beta=case_dict['input']['beta'],
            kappa=case_dict['input']['kappa']
        )

        assert epsilon == case_dict['output'], f'Expansibility calculation failed for {case}'


def test_calculate_C_orifice_ReaderHarrisGallagher():
    '''
    Validate calculate_C_orifice_ReaderHarrisGallagher function.
    The function has been tested on a number of known cases. 
    Then these test cases have been generated, to cover a wider range of possible inputs.
    '''
    cases = {
        'case1': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6210967127147193},
        'case2': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 1000, 'tapping': 'D'}, 'output': 0.620781324667837},
        'case3': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.620781324667837},
        'case4': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6206681362922947},
        'case5': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6079414386218523},
        'case6': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6076268390168605},
        'case7': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6076268390168605},
        'case8': {'input': {'D': 0.03, 'beta': 0.1, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6075136469147502},
        'case9': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6865943739462489},
        'case10': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 1000, 'tapping': 'D'}, 'output': 0.684049053085603},
        'case11': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.684049053085603},
        'case12': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6834422723627231},
        'case13': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6066508732223671},
        'case14': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6060101840402702},
        'case15': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6060101840402702},
        'case16': {'input': {'D': 0.03, 'beta': 0.5, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.605394401081893},
        'case17': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.9022964047296906},
        'case18': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 1000, 'tapping': 'D'}, 'output': 0.8959768646813352},
        'case19': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.8959768646813352},
        'case20': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.9013159878271764},
        'case21': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5777936160635622},
        'case22': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6003417537063434},
        'case23': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6003417537063434},
        'case24': {'input': {'D': 0.03, 'beta': 0.8, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6055444338665065},
        'case25': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6095215946044831},
        'case26': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 1000, 'tapping': 'D'}, 'output': 0.6092062065576007},
        'case27': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.6092062065576007},
        'case28': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6092749894521301},
        'case29': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5963663205116161},
        'case30': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.5960517209066243},
        'case31': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.5960517209066243},
        'case32': {'input': {'D': 0.08, 'beta': 0.1, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5961203223038438},
        'case33': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6821424054423119},
        'case34': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 1000, 'tapping': 'D'}, 'output': 0.679597084581666},
        'case35': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.679597084581666},
        'case36': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6799888571052785},
        'case37': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6021989047184301},
        'case38': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6015582155363332},
        'case39': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6015582155363332},
        'case40': {'input': {'D': 0.08, 'beta': 0.5, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6015115467113069},
        'case41': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.903186798430478},
        'case42': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 1000, 'tapping': 'D'}, 'output': 0.8968672583821226},
        'case43': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.8968672583821226},
        'case44': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.8963558457105707},
        'case45': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5786840097643495},
        'case46': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6012321474071307},
        'case47': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6012321474071307},
        'case48': {'input': {'D': 0.08, 'beta': 0.8, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5940754690490321},
        'case49': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6095215946044831},
        'case50': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 1000, 'tapping': 'D'}, 'output': 0.6092062065576007},
        'case51': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.6092062065576007},
        'case52': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6093349742318511},
        'case53': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5963663205116161},
        'case54': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.5960517209066243},
        'case55': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.5960517209066243},
        'case56': {'input': {'D': 0.12, 'beta': 0.1, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5961801538457855},
        'case57': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6821424054423119},
        'case58': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 1000, 'tapping': 'D'}, 'output': 0.679597084581666},
        'case59': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.679597084581666},
        'case60': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6804190839724089},
        'case61': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6021989047184301},
        'case62': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6015582155363332},
        'case63': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6015582155363332},
        'case64': {'input': {'D': 0.12, 'beta': 0.5, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6015715985124956},
        'case65': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.903186798430478},
        'case66': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 1000, 'tapping': 'D'}, 'output': 0.8968672583821226},
        'case67': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.8968672583821226},
        'case68': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.8969362419379183},
        'case69': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5786840097643495},
        'case70': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6012321474071307},
        'case71': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6012321474071307},
        'case72': {'input': {'D': 0.12, 'beta': 0.8, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.58904528207898},
        'case73': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6095215946044831},
        'case74': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'D'}, 'output': 0.6092062065576007},
        'case75': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.6092062065576007},
        'case76': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6094594201422464},
        'case77': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5963663205116161},
        'case78': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.5960517209066243},
        'case79': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.5960517209066243},
        'case80': {'input': {'D': 0.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5963042369168906},
        'case81': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6821424054423119},
        'case82': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'D'}, 'output': 0.679597084581666},
        'case83': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.679597084581666},
        'case84': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6814392890350428},
        'case85': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6021989047184301},
        'case86': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6015582155363332},
        'case87': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6015582155363332},
        'case88': {'input': {'D': 0.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6017152961053875},
        'case89': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.903186798430478},
        'case90': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'D'}, 'output': 0.8968672583821226},
        'case91': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.8968672583821226},
        'case92': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.9003151541289556},
        'case93': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5786840097643495},
        'case94': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6012321474071307},
        'case95': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6012321474071307},
        'case96': {'input': {'D': 0.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5791393500582181},
        'case97': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6095215946044831},
        'case98': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'D'}, 'output': 0.6092062065576007},
        'case99': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.6092062065576007},
        'case100': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6094969278344043},
        'case101': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5963663205116161},
        'case102': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.5960517209066243},
        'case103': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.5960517209066243},
        'case104': {'input': {'D': 1.5, 'beta': 0.1, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.5963416773970021},
        'case105': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.6821424054423119},
        'case106': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'D'}, 'output': 0.679597084581666},
        'case107': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.679597084581666},
        'case108': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.6818394792626169},
        'case109': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.6021989047184301},
        'case110': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6015582155363332},
        'case111': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6015582155363332},
        'case112': {'input': {'D': 1.5, 'beta': 0.5, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.6019531228229874},
        'case113': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'corner'}, 'output': 0.903186798430478},
        'case114': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'D'}, 'output': 0.8968672583821226},
        'case115': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'D/2'}, 'output': 0.8968672583821226},
        'case116': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 1000, 'tapping': 'flange'}, 'output': 0.9019166312342929},
        'case117': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'corner'}, 'output': 0.5786840097643495},
        'case118': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D'}, 'output': 0.6012321474071307},
        'case119': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'D/2'}, 'output': 0.6012321474071307},
        'case120': {'input': {'D': 1.5, 'beta': 0.8, 'Re': 110000000, 'tapping': 'flange'}, 'output': 0.578279953742449},
        }

    for case, case_dict in cases.items():
        C = differential_pressure_flowmeters.calculate_C_orifice_ReaderHarrisGallagher(
            D=case_dict['input']['D'],
            beta=case_dict['input']['beta'],
            Re=case_dict['input']['Re'],
            tapping=case_dict['input']['tapping']
        )
        
        rel_dev = utilities.calculate_relative_deviation(C, case_dict['output'])

        assert rel_dev < 0.0000001, f'Case {case} failed. Relative deviation: {rel_dev}'
        


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


def test_calculate_flow_orifice_complete():
    # Test orifice calculation for a single case, including calculation of beta, epsilon, C and flowrates

    data={
        'D': 0.3, # m
        'd': 0.1, # m
        'dP': 280.0, # mbar
        'rho1': 15.0,
        'mu': 1.12e-05,
        'C': 0.599031,
        'kappa': 1.2,
        'VolFlow': 1037.019349,
        'MassFlow': 15555.29024,
        'Re': 1637368.6064174655,
        'Velocity': 4.075229,
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
    
    assert round(C,6) == data['C'], 'Discharge coefficient calculation failed'

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
    
    print(res)

    # Check that calculated C is equal to the actual C
    assert round(res['C'],6) == data['C'], 'Discharge coefficient calculation failed'

    assert round(res['MassFlow'],6) == data['MassFlow'], 'Mass flow from orifice calculation failed'

    assert round(res['VolFlow'],6) == data['VolFlow'], 'Volume flow from orifice calculation failed'

    assert round(res['Velocity'],6) == data['Velocity'], 'Velocity from orifice calculation failed'


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
