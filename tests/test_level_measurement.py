from pvtlib.metering import level_measurement
import numpy as np

def test_level_from_differential_pressure():

    cases = {
        'case1': {'dP': 198.162, 'rho1': 20, 'rho2': 1000, 'h': 3, 'expected_h2': 2},
        'case2': {'dP': 981.000, 'rho1': 0, 'rho2': 1000, 'h': 10, 'expected_h2': 10},
        'case3': {'dP': 137.340, 'rho1': 100, 'rho2': 650, 'h': 3, 'expected_h2': 2},
        'case4': {'dP': 64.256, 'rho1': 650, 'rho2': 1050, 'h': 0.7, 'expected_h2': 0.5},
        'case5': {'dP': 16.187, 'rho1': 1, 'rho2': 650, 'h': 100.1, 'expected_h2': 0.1}
    }

    for case_name, case_dict in cases.items():
        h2 = level_measurement.level_from_differential_pressure(
            dP=case_dict['dP'],
            rho1=case_dict['rho1'],
            rho2=case_dict['rho2'],
            h=case_dict['h']
        )

        abs_diff = abs(h2 - case_dict['expected_h2'])

        assert abs_diff < 0.01, f'Failed for case {case_name}. Expected h2: {case_dict["expected_h2"]}, got h2: {h2}'


def test_level_from_differential_pressure_invalid_input():
    cases = {
        'case1': {'dP': -198.162, 'rho1': 20, 'rho2': 1000, 'h': 3, 'expected_h2': 2},
        'case2': {'dP': 981.000, 'rho1': 1005, 'rho2': 1000, 'h': 10, 'expected_h2': 10},
        'case3': {'dP': 137.340, 'rho1': 100, 'rho2': 650, 'h': -3, 'expected_h2': 2}
    }
    
    for case_name, case_dict in cases.items():
        h2 = level_measurement.level_from_differential_pressure(
            dP=case_dict['dP'],
            rho1=case_dict['rho1'],
            rho2=case_dict['rho2'],
            h=case_dict['h'],
            check_input=False # Disable input checking, so that np.nan is returned
        )

        assert np.isnan(h2), f'Failed for case {case_name}. Expected nan, got h2: {h2}'

def test_static_fluid_pressure():
    cases = {
        'case1' : {'rho': 1000, 'h': 10, 'pressure_unit': 'mbar', 'expected_pressure': 980.665},
        'case2' : {'rho': 1000, 'h': 10, 'pressure_unit': 'Pa', 'expected_pressure': 98066.5},
        'case3' : {'rho': 1000, 'h': 10, 'pressure_unit': 'bar', 'expected_pressure': 0.980665},
    }

    for case_name, case_dict in cases.items():
        pressure = level_measurement.static_fluid_pressure(
            rho=case_dict['rho'],
            h=case_dict['h'],
            pressure_unit=case_dict['pressure_unit']
        )

        abs_diff = abs(pressure - case_dict['expected_pressure'])

        assert abs_diff < 0.01, f'Failed for case {case_name}. Expected pressure: {case_dict["expected_pressure"]}, got pressure: {pressure}'

