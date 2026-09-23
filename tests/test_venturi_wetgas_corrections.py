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

from pvtlib.metering import differential_pressure_flowmeters


def test_calculate_C_wetgas_venturi_ReaderHarrisGraham():
    """
    Test the calculate_C_wetgas_venturi_ReaderHarrisGraham function.
    """

    cases= [
        {'X': 0.2, 'Fr_gas': 17.0, 'expected': 0.980210688650774},
        {'X': 0.1, 'Fr_gas': 12.0, 'expected': 0.9745900212488465},
        {'X': 0.2, 'Fr_gas': 8.0, 'expected': 0.9689641818685499},
        {'X': 0.3, 'Fr_gas': 5.0, 'expected': 0.9639415237437939},
        {'X': 0.05, 'Fr_gas': 3.0, 'expected': 0.9601492206915199}
    ]

    for i, case in enumerate(cases):
        C = differential_pressure_flowmeters.calculate_C_wetgas_venturi_ReaderHarrisGraham(case["Fr_gas"], case["X"])
        assert np.isclose(C, case["expected"], rtol=1e-6), f"Case {i+1}: got {C}, expected {case['expected']}"

def test_calculate_C_wetgas_venturi_ReaderHarrisGraham_invalid_inputs():
    """
    Test the calculate_C_wetgas_venturi_ReaderHarrisGraham function for invalid input handling.
    """
    # X < 0
    assert np.isnan(differential_pressure_flowmeters.calculate_C_wetgas_venturi_ReaderHarrisGraham(10, -0.1))
    # Fr_gas < 0
    assert np.isnan(differential_pressure_flowmeters.calculate_C_wetgas_venturi_ReaderHarrisGraham(-5, 0.5))


def test_calculate_flow_wetgas_venturi_ReaderHarrisGraham():
    """
    Regression cases for the wet-gas venturi calculation.

    The expected values were regenerated after the shared Froude number
    started using the standard acceleration of free fall,
    g_n = 9.806 65 m/s2, in place of the previous 9.81 m/s2. The largest
    relative change is 1.7e-4 in Fr_gas, and 3.8e-6 in the corrected gas
    mass flow. The case04 iteration count changed from 3 to 4.

    TODO: Quality Check. These are regression values produced by this
    implementation, not independently calculated expected values.
    """
    cases = {
        'case01': {  # TODO: Quality Check
            'input': {
                'D': 0.12,  # Pipe diameter [m]
                'd': 0.08,  # Throat diameter [m]
                'P1': 50.0,  # Upstream pressure [bara]
                'dP': 450,  # Differential pressure [mbar]
                'rho_g': 40.0,  # Gas density [kg/m3]
                'rho_l': 850.0,  # Liquid density [kg/m3]
                'GMF': 0.6666666666667,  # Gas mass fraction [-]
                'kappa': 1.3,  # Isentropic exponent [-]
                'check_input': False,  # Input validity checking [bool]
            },
            'expected': {
                'MassFlow_gas_initial': 38063.304281883706,  # Uncorrected gas mass flow [kg/h]
                'MassFlow_gas_corrected': 30217.40819562645,  # Corrected gas mass flow [kg/h]
                'MassFlow_liq': 15108.704097810956,  # Liquid mass flow [kg/h]
                'MassFlow_tot': 45326.11229343741,  # Total mass flow [kg/h]
                'VolFlow_gas': 755.4352048906612,  # Gas volume flow [m3/h]
                'VolFlow_liq': 17.774945997424656,  # Liquid volume flow [m3/h]
                'VolFlow_tot': 773.2101508880859,  # Total volume flow [m3/h]
                'OverRead': 1.2251025816879337,  # Over-read factor [-]
                'C_wet': 0.9725751741947309,  # Wet-gas discharge coefficient [-]
                'LockhartMartinelli': 0.10846522890931178,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 3.8008337272553696,  # Gas densimetric Froude number [-]
                'Fr_gas_th': 10.473866132553429,  # Throat gas densimetric Froude number [-]
                'n': 0.47536986881430643,  # Correlation exponent [-]
                'C_Ch': 4.50938641530033,  # Chisholm coefficient [-]
                'epsilon': 0.993109300625241,  # Expansibility factor [-]
                'iterations': 6,  # Iteration count [-]
            },
        },
        'case02': {  # TODO: Quality Check
            'input': {
                'D': 0.12,  # Pipe diameter [m]
                'd': 0.08,  # Throat diameter [m]
                'P1': 50.0,  # Upstream pressure [bara]
                'dP': 550,  # Differential pressure [mbar]
                'rho_g': 50.0,  # Gas density [kg/m3]
                'rho_l': 850.0,  # Liquid density [kg/m3]
                'GMF': 0.6666666666667,  # Gas mass fraction [-]
                'kappa': 1.3,  # Isentropic exponent [-]
                'check_input': False,  # Input validity checking [bool]
            },
            'expected': {
                'MassFlow_gas_initial': 46975.033547223604,  # Uncorrected gas mass flow [kg/h]
                'MassFlow_gas_corrected': 37089.00983549633,  # Corrected gas mass flow [kg/h]
                'MassFlow_liq': 18544.504917745377,  # Liquid mass flow [kg/h]
                'MassFlow_tot': 55633.5147532417,  # Total mass flow [kg/h]
                'VolFlow_gas': 741.7801967099265,  # Gas volume flow [m3/h]
                'VolFlow_liq': 21.817064609112208,  # Liquid volume flow [m3/h]
                'VolFlow_tot': 763.5972613190387,  # Total volume flow [m3/h]
                'OverRead': 1.2336663867176625,  # Over-read factor [-]
                'C_wet': 0.9740379366561818,  # Wet-gas discharge coefficient [-]
                'LockhartMartinelli': 0.12126781251814828,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 4.198647439122112,  # Gas densimetric Froude number [-]
                'Fr_gas_th': 11.570111815154027,  # Throat gas densimetric Froude number [-]
                'n': 0.48290128430254337,  # Correlation exponent [-]
                'C_Ch': 4.182699933571969,  # Chisholm coefficient [-]
                'epsilon': 0.9915795625474295,  # Expansibility factor [-]
                'iterations': 5,  # Iteration count [-]
            },
        },
        'case03': {  # TODO: Quality Check
            'input': {
                'D': 0.12,  # Pipe diameter [m]
                'd': 0.08,  # Throat diameter [m]
                'P1': 50.0,  # Upstream pressure [bara]
                'dP': 650,  # Differential pressure [mbar]
                'rho_g': 60.0,  # Gas density [kg/m3]
                'rho_l': 850.0,  # Liquid density [kg/m3]
                'GMF': 0.6666666666667,  # Gas mass fraction [-]
                'kappa': 1.3,  # Isentropic exponent [-]
                'check_input': False,  # Input validity checking [bool]
            },
            'expected': {
                'MassFlow_gas_initial': 55855.09273617424,  # Uncorrected gas mass flow [kg/h]
                'MassFlow_gas_corrected': 43920.497433799384,  # Corrected gas mass flow [kg/h]
                'MassFlow_liq': 21960.248716896393,  # Liquid mass flow [kg/h]
                'MassFlow_tot': 65880.74615069578,  # Total mass flow [kg/h]
                'VolFlow_gas': 732.008290563323,  # Gas volume flow [m3/h]
                'VolFlow_liq': 25.83558672576046,  # Liquid volume flow [m3/h]
                'VolFlow_tot': 757.8438772890835,  # Total volume flow [m3/h]
                'OverRead': 1.2403507699164902,  # Over-read factor [-]
                'C_wet': 0.9753241851095644,  # Wet-gas discharge coefficient [-]
                'LockhartMartinelli': 0.13284223283099433,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 4.567433619678333,  # Gas densimetric Froude number [-]
                'Fr_gas_th': 12.586367027525755,  # Throat gas densimetric Froude number [-]
                'n': 0.4880363044178782,  # Correlation exponent [-]
                'C_Ch': 3.9206129143546664,  # Chisholm coefficient [-]
                'epsilon': 0.9900503659309642,  # Expansibility factor [-]
                'iterations': 4,  # Iteration count [-]
            },
        },
        'case04': {  # TODO: Quality Check
            'input': {
                'D': 0.12,  # Pipe diameter [m]
                'd': 0.08,  # Throat diameter [m]
                'P1': 50.0,  # Upstream pressure [bara]
                'dP': 750,  # Differential pressure [mbar]
                'rho_g': 70.0,  # Gas density [kg/m3]
                'rho_l': 850.0,  # Liquid density [kg/m3]
                'GMF': 0.6666666666667,  # Gas mass fraction [-]
                'kappa': 1.3,  # Isentropic exponent [-]
                'check_input': False,  # Input validity checking [bool]
            },
            'expected': {
                'MassFlow_gas_initial': 64705.17944668863,  # Uncorrected gas mass flow [kg/h]
                'MassFlow_gas_corrected': 50711.73731951213,  # Corrected gas mass flow [kg/h]
                'MassFlow_liq': 25355.868659752257,  # Liquid mass flow [kg/h]
                'MassFlow_tot': 76067.6059792644,  # Total mass flow [kg/h]
                'VolFlow_gas': 724.4533902787448,  # Gas volume flow [m3/h]
                'VolFlow_liq': 29.830433717355596,  # Liquid volume flow [m3/h]
                'VolFlow_tot': 754.2838239961004,  # Total volume flow [m3/h]
                'OverRead': 1.2459227748343158,  # Over-read factor [-]
                'C_wet': 0.9764737385490545,  # Wet-gas discharge coefficient [-]
                'LockhartMartinelli': 0.14348601079586634,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 4.913673922561178,  # Gas densimetric Froude number [-]
                'Fr_gas_th': 13.540493106781634,  # Throat gas densimetric Froude number [-]
                'n': 0.4916566152724167,  # Correlation exponent [-]
                'C_Ch': 3.7058339179365376,  # Chisholm coefficient [-]
                'epsilon': 0.9885217041581938,  # Expansibility factor [-]
                'iterations': 4,  # Iteration count [-]
            },
        },
        'case05': {  # TODO: Quality Check
            'input': {
                'D': 0.12,  # Pipe diameter [m]
                'd': 0.08,  # Throat diameter [m]
                'P1': 50.0,  # Upstream pressure [bara]
                'dP': 850,  # Differential pressure [mbar]
                'rho_g': 80.0,  # Gas density [kg/m3]
                'rho_l': 850.0,  # Liquid density [kg/m3]
                'GMF': 0.6666666666667,  # Gas mass fraction [-]
                'kappa': 1.3,  # Isentropic exponent [-]
                'check_input': False,  # Input validity checking [bool]
            },
            'expected': {
                'MassFlow_gas_initial': 73526.17355917922,  # Uncorrected gas mass flow [kg/h]
                'MassFlow_gas_corrected': 57461.31306303752,  # Corrected gas mass flow [kg/h]
                'MassFlow_liq': 28730.656531514443,  # Liquid mass flow [kg/h]
                'MassFlow_tot': 86191.96959455196,  # Total mass flow [kg/h]
                'VolFlow_gas': 718.266413287969,  # Gas volume flow [m3/h]
                'VolFlow_liq': 33.800772390016995,  # Liquid volume flow [m3/h]
                'VolFlow_tot': 752.067185677986,  # Total volume flow [m3/h]
                'OverRead': 1.2508039603553947,  # Over-read factor [-]
                'C_wet': 0.97751364537718,  # Wet-gas discharge coefficient [-]
                'LockhartMartinelli': 0.15339299776945103,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 5.241786823849905,  # Gas densimetric Froude number [-]
                'Fr_gas_th': 14.444665941235895,  # Throat gas densimetric Froude number [-]
                'n': 0.4942754193003023,  # Correlation exponent [-]
                'C_Ch': 3.526765519565194,  # Chisholm coefficient [-]
                'epsilon': 0.9869935706113948,  # Expansibility factor [-]
                'iterations': 5,  # Iteration count [-]
            },
        },
    }

    for case_name, case in cases.items():
        res = differential_pressure_flowmeters.calculate_flow_wetgas_venturi_ReaderHarrisGraham(
            D=case['input']['D'],
            d=case['input']['d'],
            P1=case['input']['P1'],
            dP=case['input']['dP'],
            rho_g=case['input']['rho_g'],
            rho_l=case['input']['rho_l'],
            GMF=case['input']['GMF'],
            kappa=case['input']['kappa'],
            check_input=case['input']['check_input']
        )

        for key in case['expected']:
            # For integer comparisons (like 'iterations'), use exact match
            if isinstance(case['expected'][key], int):
                assert res[key] == case['expected'][key], f"Case {case_name}: {key} mismatch: got {res[key]}, expected {case['expected'][key]}"
            else:
                assert np.isclose(res[key], case['expected'][key], rtol=1e-8), f"Case {case_name}: {key} mismatch: got {res[key]}, expected {case['expected'][key]}"


def test_calculate_flow_wetgas_venturi_ReaderHarrisGraham_invalid_inputs():
    """
    Test calculate_flow_wetgas_venturi_ReaderHarrisGraham for invalid input handling.
    Should return all np.nan in results if check_input=False, or raise Exception if check_input=True.
    """
    func = differential_pressure_flowmeters.calculate_flow_wetgas_venturi_ReaderHarrisGraham

    # List of invalid input cases (all should return np.nan for all outputs)
    invalid_cases = [
        # D <= 0
        dict(D=0, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # d <= 0
        dict(D=0.1, d=0, P1=60, dP=500, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # d >= D (throat diameter equal to or larger than pipe diameter)
        dict(D=0.1, d=0.1, P1=60, dP=500, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        dict(D=0.1, d=0.12, P1=60, dP=500, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # P1 <= 0
        dict(D=0.1, d=0.06, P1=0, dP=500, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # dP < 0
        dict(D=0.1, d=0.06, P1=60, dP=-1, rho_g=50, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # rho_g <= 0
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=0, rho_l=800, GMF=0.7, kappa=1.3, check_input=False),
        # rho_l <= 0
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=0, GMF=0.7, kappa=1.3, check_input=False),
        # GMF not in (0,1]
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=0, kappa=1.3, check_input=False),
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=1.1, kappa=1.3, check_input=False),
        # GVF not in (0,1]
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=None, GVF=0, kappa=1.3, check_input=False),
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=None, GVF=1.1, kappa=1.3, check_input=False),
        # Both GMF and GVF None
        dict(D=0.1, d=0.06, P1=60, dP=500, rho_g=50, rho_l=800, GMF=None, GVF=None, kappa=1.3, check_input=False),
    ]

    for i, case in enumerate(invalid_cases):
        res = func(**case)
        for key, val in res.items():
            assert np.isnan(val), f"Case {i+1} failed for key {key}: expected np.nan, got {val}"
