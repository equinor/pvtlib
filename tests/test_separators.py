from pvtlib.equipment import separators

import numpy as np

def test_scrubber_K_value():
    '''
    Function that tests the scrubber K-value calcualtion.
    Also checks the cases where gas and liquid densities are equal, gas density is negative and gas density larger than liquid density. They should return nan
    '''
    test_data = {
        'case_01' : {'Usg' : 5.0, 'rho_gas' : 50.0, 'rho_liquid' : 700.0, 'K' : 1.386750490563073},
        'case_02' : {'Usg' : 50.0, 'rho_gas' : 10.0, 'rho_liquid' : 1000.0, 'K' : 5.02518907629606},
        'case_03' : {'Usg' : 50.0, 'rho_gas' : 200.0, 'rho_liquid' : 200.0, 'K' : np.nan},
        'case_04' : {'Usg' : 50.0, 'rho_gas' : -200.0, 'rho_liquid' : 200.0, 'K' : np.nan},
        'case_05' : {'Usg' : 50.0, 'rho_gas' : 400.0, 'rho_liquid' : 200.0, 'K' : np.nan},
        'case_06' : {'Usg' : 0.1453, 'rho_gas' : 135.0, 'rho_liquid' : 565.0, 'K' : 0.08141384588831056} #from Guard process calculations
        }
    
    for name, icase in test_data.items():
        result = separators.scrubber_K_value(
            Usg=icase['Usg'], 
            rho_gas=icase['rho_gas'], 
            rho_liquid=icase['rho_liquid']
            )
        if np.isnan(icase['K']):
            assert np.isnan(result), f'ERROR: Scrubber K-value calculation failed for {name}'
        else:
            assert result == icase['K'], f'ERROR: Scrubber K-value calculation failed for {name}'


def test_scrubber_inlet_momentum():
    '''
    Function that tests the scrubber inlet momentum calcualtion.
    '''
    test_data = {
        'case_01' : {'u' : 25.0, 'rho' : 70.0, 'IM' : 43750.0},
        'case_02' : {'u' : 1.0, 'rho' : 700.0, 'IM' : 700.0},
        'case_03' : {'u' : np.nan, 'rho' : 700.0, 'IM' : np.nan},
        'case_04' : {'u' : 5.0, 'rho' : np.nan, 'IM' : np.nan},
        'case_05' : {'u' : 7.365, 'rho' : 156.5, 'IM' : 8489.0647125} #from Guard process calculations
        }

    for name, icase in test_data.items():
        result = separators.scrubber_inlet_momentum(
            u=icase['u'], 
            rho=icase['rho']
            )
        if np.isnan(icase['IM']):
            assert np.isnan(result), f'ERROR: Scrubber inlet momentum calculation failed for {name}'
        else:
            assert result == icase['IM'], f'ERROR: Scrubber inlet momentum calculation failed for {name}'