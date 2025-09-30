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

def test_gas_densiometric_Froude_number_cases():
    """
    Test _gas_densiometric_Froude_number for a variety of various wet-gas cases.
    """
    cases = {
        1: {'massflow_gas': 7.5, 'D': 0.2, 'rho_g': 50, 'rho_l': 800.0, 'Frg_expected': 0.8801288463948925},
        2: {'massflow_gas': 5.5, 'D': 0.3, 'rho_g': 50, 'rho_l': 800.0, 'Frg_expected': 0.2342176039238587},
        3: {'massflow_gas': 6.5, 'D': 0.4, 'rho_g': 50, 'rho_l': 1000.0, 'Frg_expected': 0.1198097573116477},
        4: {'massflow_gas': 7.0, 'D': 0.1, 'rho_g': 60, 'rho_l': 850.0, 'Frg_expected': 4.133181569369208},
        5: {'massflow_gas': 4.5, 'D': 0.1, 'rho_g': 55, 'rho_l': 600.0, 'Frg_expected': 3.341246623081836},
        6: {'massflow_gas': 8.0, 'D': 0.15, 'rho_g': 70, 'rho_l': 950.0, 'Frg_expected': 1.5036511757580975},
        7: {'massflow_gas': 3.0, 'D': 0.05, 'rho_g': 40, 'rho_l': 800.0, 'Frg_expected': 12.512240026690062},
        8: {'massflow_gas': 9.5, 'D': 0.12, 'rho_g': 65, 'rho_l': 1000.0, 'Frg_expected': 3.140390257409154},
        9: {'massflow_gas': 5.5, 'D': 0.1, 'rho_g': 75, 'rho_l': 800.0, 'Frg_expected': 3.0320661323698928},
        10: {'massflow_gas': 6.0, 'D': 0.1, 'rho_g': 45, 'rho_l': 700.0, 'Frg_expected': 4.492622816820113},
    }

    for i, case in cases.items():
        Frg = differential_pressure_flowmeters._gas_densiometric_Froude_number(
            massflow_gas=case['massflow_gas'],
            D=case['D'],
            rho_g=case['rho_g'],
            rho_l=case['rho_l']
        )
        assert np.isclose(Frg, case['Frg_expected'], rtol=1e-8), f"Case {i}: Froude number mismatch: got {Frg}, expected {case['Frg_expected']}"

def test_gas_densiometric_Froude_number_invalid_inputs():
    """
    Test _gas_densiometric_Froude_number for invalid input handling.
    """
    # D <= 0
    assert np.isnan(differential_pressure_flowmeters._gas_densiometric_Froude_number(1, 0, 10, 100))
    # rho_g <= 0
    assert np.isnan(differential_pressure_flowmeters._gas_densiometric_Froude_number(1, 0.1, 0, 100))
    # rho_l <= 0
    assert np.isnan(differential_pressure_flowmeters._gas_densiometric_Froude_number(1, 0.1, 10, 0))
    # massflow_gas < 0
    assert np.isnan(differential_pressure_flowmeters._gas_densiometric_Froude_number(-1, 0.1, 10, 100))
    # rho_l - rho_g == 0
    assert np.isnan(differential_pressure_flowmeters._gas_densiometric_Froude_number(1, 0.1, 100, 100))


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
    cases = {
        'case01': {'input': {'D': 0.12, 'd': 0.08, 'P1': 50.0, 'dP': 450, 'rho_g': 40.0, 'rho_l': 850.0, 'GMF': 0.6666666666667, 'kappa': 1.3, 'check_input': False},
                   'expected': {'MassFlow_gas_initial': 38063.304281883706, 'MassFlow_gas_corrected': 30217.522925625468, 'MassFlow_liq': 15108.761462810464, 'MassFlow_tot': 45326.28438843593, 'VolFlow_gas': 755.4380731406367, 'VolFlow_liq': 17.77501348565937, 'VolFlow_tot': 773.213086626296, 'OverRead': 1.2250949095211476, 'C_wet': 0.9725727761407659, 'LockhartMartinelli': 0.10846522890931178, 'Fr_gas': 3.8001991303710585, 'Fr_gas_th': 10.47211738917464, 'n': 0.47535583805692694, 'C_Ch': 4.509213103318227, 'epsilon': 0.993109300625241, 'iterations': 6}},
        'case02': {'input': {'D': 0.12, 'd': 0.08, 'P1': 50.0, 'dP': 550, 'rho_g': 50.0, 'rho_l': 850.0, 'GMF': 0.6666666666667, 'kappa': 1.3, 'check_input': False},
                   'expected': {'MassFlow_gas_initial': 46975.033547223604, 'MassFlow_gas_corrected': 37089.08852152743, 'MassFlow_liq': 18544.54426076093, 'MassFlow_tot': 55633.63278228836, 'VolFlow_gas': 741.7817704305486, 'VolFlow_liq': 21.817110895012856, 'VolFlow_tot': 763.5988813255615, 'OverRead': 1.2336605613787315, 'C_wet': 0.9740354037319746, 'LockhartMartinelli': 0.12126781251814828, 'Fr_gas': 4.197939389569316, 'Fr_gas_th': 11.568160660022452, 'n': 0.48288989636823004, 'C_Ch': 4.1825814106479715, 'epsilon': 0.9915795625474295, 'iterations': 5}},
        'case03': {'input': {'D': 0.12, 'd': 0.08, 'P1': 50.0, 'dP': 650, 'rho_g': 60.0, 'rho_l': 850.0, 'GMF': 0.6666666666667, 'kappa': 1.3, 'check_input': False},
                   'expected': {'MassFlow_gas_initial': 55855.09273617424, 'MassFlow_gas_corrected': 43920.53612074391, 'MassFlow_liq': 21960.26806036866, 'MassFlow_tot': 65880.80418111257, 'VolFlow_gas': 732.0089353457319, 'VolFlow_liq': 25.83560948278666, 'VolFlow_tot': 757.8445448285186, 'OverRead': 1.2403463223282916, 'C_wet': 0.9753215469423092, 'LockhartMartinelli': 0.13284223283099433, 'Fr_gas': 4.566657713062191, 'Fr_gas_th': 12.584228880315958, 'n': 0.48802701319020325, 'C_Ch': 3.9205298600512526, 'epsilon': 0.9900503659309642, 'iterations': 4}},
        'case04': {'input': {'D': 0.12, 'd': 0.08, 'P1': 50.0, 'dP': 750, 'rho_g': 70.0, 'rho_l': 850.0, 'GMF': 0.6666666666667, 'kappa': 1.3, 'check_input': False},
                   'expected': {'MassFlow_gas_initial': 64705.17944668863, 'MassFlow_gas_corrected': 50711.735110735375, 'MassFlow_liq': 25355.86755536388, 'MassFlow_tot': 76067.60266609925, 'VolFlow_gas': 724.4533587247911, 'VolFlow_liq': 29.83043241807515, 'VolFlow_tot': 754.2837911428662, 'OverRead': 1.2459193576866787, 'C_wet': 0.9764710178788921, 'LockhartMartinelli': 0.14348601079586634, 'Fr_gas': 4.9128346564015475, 'Fr_gas_th': 13.53818036120097, 'n': 0.491648996619922, 'C_Ch': 3.7057745742248547, 'epsilon': 0.9885217041581938, 'iterations': 3}},
        'case05': {'input': {'D': 0.12, 'd': 0.08, 'P1': 50.0, 'dP': 850, 'rho_g': 80.0, 'rho_l': 850.0, 'GMF': 0.6666666666667, 'kappa': 1.3, 'check_input': False},
                   'expected': {'MassFlow_gas_initial': 73526.17355917922, 'MassFlow_gas_corrected': 57461.27070391029, 'MassFlow_liq': 28730.63535195083, 'MassFlow_tot': 86191.90605586112, 'VolFlow_gas': 718.2658837988786, 'VolFlow_liq': 33.80074747288333, 'VolFlow_tot': 752.0666312717619, 'OverRead': 1.2508013183707996, 'C_wet': 0.9775108600458319, 'LockhartMartinelli': 0.15339299776945103, 'Fr_gas': 5.240887879590297, 'Fr_gas_th': 14.442188742149748, 'n': 0.4942691427142624, 'C_Ch': 3.526722432835647, 'epsilon': 0.9869935706113948, 'iterations': 5}}
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
