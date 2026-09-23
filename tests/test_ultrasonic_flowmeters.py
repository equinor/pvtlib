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

import re
from math import pi, sqrt

import numpy as np
import pytest

from pvtlib import fluid_mechanics
from pvtlib.metering import ultrasonic_flowmeters


# Equation references: van Putten et al., NSFMW 2015. The numerical expectations
# below are calculated equation checks, not measurements. Each case remains
# marked TODO: Quality Check until manually verified.
# https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf

# Result keys that are not numerical, and therefore not checked for nan or finiteness
DIAGNOSTIC_KEYS = {'within_JIP_envelope', 'JIP_envelope_exceeded', 'error'}

NUMERICAL_KEYS = {
    'VolFlow_gas_measured', 'VolFlow_gas_corrected', 'VolFlow_liq', 'VolFlow_tot',
    'MassFlow_gas', 'MassFlow_liq', 'OverRead', 'alpha_gas', 'LockhartMartinelli',
    'Fr_gas', 'Fr_gas_crit', 'GVF', 'GMF', 'DR', 'iterations',
}


#%% Tests of the individual Van Putten equations

def test_gas_void_fraction_low_froude_VanPutten_2015():
    """
    Test the low Froude gas void fraction, equation 30.

    The expected values were calculated outside pvtlib using the decimal module
    at 50 digit precision. Dry gas (X = 0) must give 1. A large X is an
    extrapolation where the equation predicts a void fraction above 1, which is
    non-physical and must give nan.
    """
    cases = {
        'Low liquid loading': { 
            'input': {'X': 0.1},  # Lockhart-Martinelli parameter [-]
            'expected': 0.8793108262159716,  # Gas void fraction [-]
        },
        'Middle of the tested range': { 
            'input': {'X': 0.25},  # [-]
            'expected': 0.8113140834123986,  # [-]
        },
        'Upper end of the tested range': { 
            'input': {'X': 0.3},  # [-]
            'expected': 0.8007218855672468,  # [-]
        },
        'Dry gas': { 
            'input': {'X': 0.0},  # [-]
            'expected': 1.0,  # [-]
        },
    }

    for name, case in cases.items():
        alpha = ultrasonic_flowmeters.gas_void_fraction_low_froude_VanPutten_2015(X=case['input']['X'])
        assert np.isclose(alpha, case['expected'], rtol=1e-13), \
            f"{name}, input={case['input']}: got {alpha}, expected {case['expected']}"

    alpha_extrapolated = ultrasonic_flowmeters.gas_void_fraction_low_froude_VanPutten_2015(X=2.0)
    assert np.isnan(alpha_extrapolated), \
        f'X=2.0 predicts a void fraction above 1, expected nan, got {alpha_extrapolated}'


def test_critical_froude_from_WLR_VanPutten_2015():
    """
    Test the critical gas Froude number from the water-liquid ratio, equation 27.
    """
    cases = {
        'Hydrocarbon liquid': {  # TODO: Quality Check
            'input': {'WLR': 0.0},  # Water fraction of liquid volume flow [-]
            'expected': 1.2,  # Critical gas Froude number [-]
        },
        'Half water': {  # TODO: Quality Check
            'input': {'WLR': 0.5},  # [-]
            'expected': 1.35,  # [-]
        },
        'Water': {  # TODO: Quality Check
            'input': {'WLR': 1.0},  # [-]
            'expected': 1.5,  # [-]
        },
    }

    for name, case in cases.items():
        Fr_gas_crit = ultrasonic_flowmeters.critical_froude_from_WLR_VanPutten_2015(WLR=case['input']['WLR'])
        assert np.isclose(Fr_gas_crit, case['expected']), \
            f"{name}, input={case['input']}: got {Fr_gas_crit}, expected {case['expected']}"


def test_critical_froude_from_Ohnesorge_VanPutten_2015():
    """
    Test the critical gas Froude number from the gas Ohnesorge number,
    equations 25 and 26.

    The expected value was calculated outside pvtlib using the decimal module
    at 45 digit precision.
    """
    cases = {
        '150 mm pipe': {  # TODO: Quality Check
            'input': {
                'rho_g': 20.0,  # Gas density [kg/m3]
                'mu_g': 1.2e-5,  # Gas dynamic viscosity [Pa.s]
                'surface_tension': 0.04,  # Gas-liquid interfacial tension [N/m]
                'D': 0.15,  # Inner pipe diameter [m]
            },
            'expected': 1.8542921112637038,  # Critical gas Froude number [-]
        },
        '200 mm pipe, heavier gas': {  # TODO: Quality Check
            'input': {
                'rho_g': 30.0,  # [kg/m3]
                'mu_g': 2.0e-5,  # [Pa.s]
                'surface_tension': 0.05,  # [N/m]
                'D': 0.2,  # [m]
            },
            'expected': 1.7498931491397873,  # [-]
        },
    }

    for name, case in cases.items():
        Fr_gas_crit = ultrasonic_flowmeters.critical_froude_from_Ohnesorge_VanPutten_2015(
            rho_g=case['input']['rho_g'],
            mu_g=case['input']['mu_g'],
            surface_tension=case['input']['surface_tension'],
            D=case['input']['D']
        )

        assert np.isclose(Fr_gas_crit, case['expected'], rtol=1e-13), \
            f"{name}, input={case['input']}: got {Fr_gas_crit}, expected {case['expected']}"


def test_gas_void_fraction_VanPutten_2015_both_branches():
    """
    Test the gas void fraction across the low and high Froude branches, equation 29.

    Below the critical Froude number the result must equal the low Froude value,
    independent of the Froude number. The two branches must meet at the critical
    Froude number. Far above it, the void fraction must approach the no-slip
    limit GVF. The high Froude expected value was calculated outside pvtlib
    using the decimal module at 45 digit precision.
    """
    cases = {
        'Well below critical Froude': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # Lockhart-Martinelli parameter [-]
                'Fr_gas': 0.7,  # Gas densimetric Froude number [-]
                'GVF': 0.975,  # Gas volume-flow fraction [-]
                'Fr_gas_crit': 1.2,  # Critical gas Froude number [-]
            },
            'expected': 0.8113140834123986,  # Gas void fraction [-]
            'rtol': 1e-13,
        },
        'Just below critical Froude': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # [-]
                'Fr_gas': 1.2 - 1e-10,  # [-]
                'GVF': 0.975,  # [-]
                'Fr_gas_crit': 1.2,  # [-]
            },
            'expected': 0.8113140834123986,  # [-]
            'rtol': 1e-13,
        },
        'At critical Froude': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # [-]
                'Fr_gas': 1.2,  # [-]
                'GVF': 0.975,  # [-]
                'Fr_gas_crit': 1.2,  # [-]
            },
            'expected': 0.8113140834123986,  # [-]
            'rtol': 1e-13,
        },
        'Just above critical Froude': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # [-]
                'Fr_gas': 1.2 + 1e-10,  # [-]
                'GVF': 0.975,  # [-]
                'Fr_gas_crit': 1.2,  # [-]
            },
            'expected': 0.8113140834123986,  # Continuity limit [-]
            'rtol': 1e-9,
        },
        'Above critical Froude': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # [-]
                'Fr_gas': 2.2,  # [-]
                'GVF': 0.975,  # [-]
                'Fr_gas_crit': 1.2,  # [-]
            },
            'expected': 0.8652780488576132,  # [-]
            'rtol': 1e-13,
        },
        'Far above critical Froude, no-slip limit': {  # TODO: Quality Check
            'input': {
                'X': 0.25,  # [-]
                'Fr_gas': 1000.0,  # [-]
                'GVF': 0.975,  # [-]
                'Fr_gas_crit': 1.2,  # [-]
            },
            'expected': 0.975,  # No-slip limit: alpha = GVF [-]
            'rtol': 1e-13,
        },
    }

    for name, case in cases.items():
        alpha = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(
            X=case['input']['X'],
            Fr_gas=case['input']['Fr_gas'],
            GVF=case['input']['GVF'],
            Fr_gas_crit=case['input']['Fr_gas_crit'],
        )
        assert np.isclose(alpha, case['expected'], rtol=case['rtol']), \
            f"{name}, input={case['input']}: got {alpha}, expected {case['expected']}"


def test_gas_void_fraction_VanPutten_2015_second_high_froude_case():
    """Check alpha_gas [-] at X = 0.1 [-] against a separate Decimal calculation."""
    # TODO: Quality Check
    alpha_second_case = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(
        X=0.1, Fr_gas=2.0, GVF=0.99, Fr_gas_crit=1.35)
    alpha_second_case_expected = 0.9046529370225384  # Gas void fraction [-]
    assert np.isclose(alpha_second_case, alpha_second_case_expected, rtol=1e-13), \
        f'X=0.1, Fr_gas=2.0, GVF=0.99, Fr_gas_crit=1.35: got {alpha_second_case}, ' \
        f'expected {alpha_second_case_expected}'


def test_gas_void_fraction_VanPutten_2015_dry_gas():
    """Check that dry gas gives alpha_gas = 1 [-] on the high Froude branch."""
    # TODO: Quality Check. All inputs and the expected output are dimensionless.
    alpha_dry = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(
        X=0.0, Fr_gas=2.2, GVF=1.0, Fr_gas_crit=1.2)
    assert alpha_dry == 1.0, f'Dry gas: got {alpha_dry}, expected 1.0'


def test_gas_void_fraction_low_froude_VanPutten_2015_negative_X():
    """Check that negative X [-] gives NaN rather than a gas void fraction."""
    # TODO: Quality Check
    result = ultrasonic_flowmeters.gas_void_fraction_low_froude_VanPutten_2015(X=-0.1)
    assert np.isnan(result), f'X=-0.1: expected nan, got {result}'


def test_critical_froude_from_WLR_VanPutten_2015_invalid_inputs():
    """Check that WLR [-] outside [0, 1] gives NaN instead of a critical Froude number."""
    cases = {
        'Negative WLR': {  # TODO: Quality Check
            'input': {'WLR': -0.1},
            'expected': np.nan,
        },
        'WLR above one': {  # TODO: Quality Check
            'input': {'WLR': 1.1},
            'expected': np.nan,
        },
    }
    for name, case in cases.items():
        result = ultrasonic_flowmeters.critical_froude_from_WLR_VanPutten_2015(WLR=case['input']['WLR'])
        assert np.isnan(result), f"{name}: expected {case['expected']}, got {result}"


def test_critical_froude_from_Ohnesorge_VanPutten_2015_invalid_inputs():
    """Check that invalid gas properties or diameter give NaN for critical Fr [-]."""
    cases = {
        'Zero gas density': {  # TODO: Quality Check
            'input': {
                'rho_g': 0.0,  # [kg/m3]
                'mu_g': 1.2e-5,  # [Pa.s]
                'surface_tension': 0.04,  # Gas-liquid [N/m]
                'D': 0.15,  # [m]
            },
            'expected': np.nan,
        },
        'Zero gas viscosity': {  # TODO: Quality Check
            'input': {
                'rho_g': 20.0,  # [kg/m3]
                'mu_g': 0.0,  # [Pa.s]
                'surface_tension': 0.04,  # [N/m]
                'D': 0.15,  # [m]
            },
            'expected': np.nan,
        },
        'Zero gas-liquid interfacial tension': {  # TODO: Quality Check
            'input': {
                'rho_g': 20.0,  # [kg/m3]
                'mu_g': 1.2e-5,  # [Pa.s]
                'surface_tension': 0.0,  # [N/m]
                'D': 0.15,  # [m]
            },
            'expected': np.nan,
        },
        'Zero diameter': {  # TODO: Quality Check
            'input': {
                'rho_g': 20.0,  # [kg/m3]
                'mu_g': 1.2e-5,  # [Pa.s]
                'surface_tension': 0.04,  # [N/m]
                'D': 0.0,  # [m]
            },
            'expected': np.nan,
        },
    }
    for name, case in cases.items():
        result = ultrasonic_flowmeters.critical_froude_from_Ohnesorge_VanPutten_2015(
            rho_g=case['input']['rho_g'],
            mu_g=case['input']['mu_g'],
            surface_tension=case['input']['surface_tension'],
            D=case['input']['D'],
        )
        assert np.isnan(result), f"{name}: expected {case['expected']}, got {result}"


def test_gas_void_fraction_VanPutten_2015_invalid_inputs():
    """Check that invalid dimensionless inputs give NaN for gas void fraction [-]."""
    cases = {
        'Negative X': {  # TODO: Quality Check
            'input': {'X': -0.1, 'Fr_gas': 1.0, 'GVF': 0.99, 'Fr_gas_crit': 1.2},
            'expected': np.nan,
        },
        'Negative gas Froude number': {  # TODO: Quality Check
            'input': {'X': 0.1, 'Fr_gas': -1.0, 'GVF': 0.99, 'Fr_gas_crit': 1.2},
            'expected': np.nan,
        },
        'Zero GVF': {  # TODO: Quality Check
            'input': {'X': 0.1, 'Fr_gas': 1.0, 'GVF': 0.0, 'Fr_gas_crit': 1.2},
            'expected': np.nan,
        },
        'GVF above one': {  # TODO: Quality Check
            'input': {'X': 0.1, 'Fr_gas': 1.0, 'GVF': 1.1, 'Fr_gas_crit': 1.2},
            'expected': np.nan,
        },
        'Zero critical gas Froude number': {  # TODO: Quality Check
            'input': {'X': 0.1, 'Fr_gas': 1.0, 'GVF': 0.99, 'Fr_gas_crit': 0.0},
            'expected': np.nan,
        },
        'X gives non-physical alpha in equation 30': {  # TODO: Quality Check
            'input': {'X': 2.0, 'Fr_gas': 1.0, 'GVF': 0.9, 'Fr_gas_crit': 1.2},
            'expected': np.nan,
        },
    }
    for name, case in cases.items():
        result = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(
            X=case['input']['X'],
            Fr_gas=case['input']['Fr_gas'],
            GVF=case['input']['GVF'],
            Fr_gas_crit=case['input']['Fr_gas_crit'],
        )
        assert np.isnan(result), f"{name}: expected {case['expected']}, got {result}"


def test_gas_void_fraction_low_froude_VanPutten_2015_nonfinite_inputs():
    """Check that non-finite X [-] gives NaN for gas void fraction [-]."""
    # TODO: Quality Check for each non-finite input.
    for X in [np.nan, np.inf, -np.inf]:
        result = ultrasonic_flowmeters.gas_void_fraction_low_froude_VanPutten_2015(X=X)
        assert np.isnan(result), f'X={X}: expected nan, got {result}'


def test_critical_froude_from_WLR_VanPutten_2015_nonfinite_inputs():
    """Check that non-finite WLR [-] gives NaN for critical gas Froude number [-]."""
    # TODO: Quality Check for each non-finite input.
    for WLR in [np.nan, np.inf, -np.inf]:
        result = ultrasonic_flowmeters.critical_froude_from_WLR_VanPutten_2015(WLR=WLR)
        assert np.isnan(result), f'WLR={WLR}: expected nan, got {result}'


def test_critical_froude_from_Ohnesorge_VanPutten_2015_nonfinite_inputs():
    """
    Check that replacing any one input with NaN or infinity gives NaN for Fr [-].

    All other inputs retain the valid values shown here.
    """
    valid_input = {
        'rho_g': 20.0,  # [kg/m3]
        'mu_g': 1.2e-5,  # [Pa.s]
        'surface_tension': 0.04,  # Gas-liquid [N/m]
        'D': 0.15,  # [m]
    }
    # TODO: Quality Check for each non-finite input.
    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            case_input = dict(valid_input)
            case_input[argument] = nonfinite
            result = ultrasonic_flowmeters.critical_froude_from_Ohnesorge_VanPutten_2015(**case_input)
            assert np.isnan(result), f'{case_input}: expected nan, got {result}'


def test_gas_void_fraction_VanPutten_2015_nonfinite_inputs():
    """Check that a non-finite dimensionless input gives NaN for gas void fraction."""
    valid_input = {
        'X': 0.1,  # [-]
        'Fr_gas': 2.0,  # [-]
        'GVF': 0.99,  # [-]
        'Fr_gas_crit': 1.2,  # [-]
    }
    # TODO: Quality Check for each non-finite input.
    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            case_input = dict(valid_input)
            case_input[argument] = nonfinite
            result = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(**case_input)
            assert np.isnan(result), f'{case_input}: expected nan, got {result}'


#%% Tests of the JIP range checks

def test_check_operating_point_DNV_USM_wetgas_JIP_2015_inclusive_limits():
    """
    Test check_operating_point_DNV_USM_wetgas_JIP_2015 at included range limits.

    All inputs are dimensionless. Each output is a boolean range check.
    """
    cases = {
        'Lower included limits': {  # TODO: Quality Check
            'input': {'GVF': 0.96, 'X': 0.0, 'DR': 0.010, 'Fr_gas': 0.7},
            'expected': {'GVF': True, 'X': True, 'DR': True, 'Fr_gas': True},
        },
        'Upper limits': {  # TODO: Quality Check
            'input': {'GVF': 1.0, 'X': 0.30, 'DR': 0.032, 'Fr_gas': 2.2},
            'expected': {'GVF': True, 'X': True, 'DR': True, 'Fr_gas': True},
        },
    }

    for name, case in cases.items():
        checks = ultrasonic_flowmeters.check_operating_point_DNV_USM_wetgas_JIP_2015(**case['input'])
        assert checks == case['expected'], f"{name}: got {checks}, expected {case['expected']}"


def test_check_operating_point_DNV_USM_wetgas_JIP_2015_outside_limits():
    """
    Test check_operating_point_DNV_USM_wetgas_JIP_2015 with one out-of-range input.

    All inputs are dimensionless. Exactly the named boolean check must fail.
    """
    cases = {
        'GVF at the excluded lower limit': {  # TODO: Quality Check
            'input': {'GVF': 0.95, 'X': 0.1, 'DR': 0.02, 'Fr_gas': 1.2},
            'expected_failed_check': 'GVF',
        },
        'GVF above one': {  # TODO: Quality Check
            'input': {'GVF': 1.01, 'X': 0.1, 'DR': 0.02, 'Fr_gas': 1.2},
            'expected_failed_check': 'GVF',
        },
        'Negative X': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': -0.01, 'DR': 0.02, 'Fr_gas': 1.2},
            'expected_failed_check': 'X',
        },
        'X above the tested range': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': 0.30001, 'DR': 0.02, 'Fr_gas': 1.2},
            'expected_failed_check': 'X',
        },
        'Density ratio below the tested range': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': 0.1, 'DR': 0.00999, 'Fr_gas': 1.2},
            'expected_failed_check': 'DR',
        },
        'Density ratio above the tested range': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': 0.1, 'DR': 0.03201, 'Fr_gas': 1.2},
            'expected_failed_check': 'DR',
        },
        'Froude number below the tested range': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': 0.1, 'DR': 0.02, 'Fr_gas': 0.69999},
            'expected_failed_check': 'Fr_gas',
        },
        'Froude number above the tested range': {  # TODO: Quality Check
            'input': {'GVF': 0.99, 'X': 0.1, 'DR': 0.02, 'Fr_gas': 2.20001},
            'expected_failed_check': 'Fr_gas',
        },
    }

    for name, case in cases.items():
        failed_check = case['expected_failed_check']
        checks = ultrasonic_flowmeters.check_operating_point_DNV_USM_wetgas_JIP_2015(**case['input'])

        assert checks[failed_check] is False, f'{name}: expected {failed_check} to be False'
        assert sum(checks.values()) == 3, \
            f'{name}: only {failed_check} should fail, got {checks}'


def test_check_operating_point_DNV_USM_wetgas_JIP_2015_nonfinite():
    """
    Test that nan, inf and -inf in all four inputs give four False checks.
    """
    # TODO: Quality Check for each non-finite input. All inputs are dimensionless.
    for nonfinite in [np.nan, np.inf, -np.inf]:
        checks = ultrasonic_flowmeters.check_operating_point_DNV_USM_wetgas_JIP_2015(
            GVF=nonfinite, X=nonfinite, DR=nonfinite, Fr_gas=nonfinite)
        assert not any(checks.values()), f'{nonfinite}: got {checks}, expected all False'


#%% Tests of the iterative flow calculation

def test_calculate_flow_wetgas_USM_VanPutten_2015_low_froude():
    """
    Test the flow calculation on the low Froude branch, where the corrected flow
    rate follows directly from the gas void fraction of equation 30.

    The densities give rho_l/rho_g = (39/4)**2, so GVF = 0.975 gives X = 0.25,
    which is the case calculated outside pvtlib.
    """
    # TODO: Quality Check. Constructed equation check, not measured fluid data.
    case_input = {
        'VolFlow_gas_measured': 100.0,  # [m3/h]
        'D': 0.2,  # [m]
        'rho_g': 16.0,  # [kg/m3]
        'rho_l': 1521.0,  # [kg/m3]
        'GVF': 0.975,  # [-]
    }
    expected = {
        'LockhartMartinelli': 0.25,  # [-]
        'alpha_gas': 0.8113140834123986,  # Equation 30, Decimal reference [-]
        'VolFlow_gas_corrected': 100.0 * 0.8113140834123986,  # [m3/h]
        'iterations': 2,
    }
    result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        **case_input, check_input=True)

    assert np.isclose(result['LockhartMartinelli'], expected['LockhartMartinelli']), \
        f"X: got {result['LockhartMartinelli']}, expected 0.25"
    assert np.isclose(result['alpha_gas'], expected['alpha_gas'], rtol=1e-12), \
        f"alpha_gas: got {result['alpha_gas']}, expected {expected['alpha_gas']}"
    assert np.isclose(result['VolFlow_gas_corrected'], expected['VolFlow_gas_corrected'], rtol=1e-12), \
        f"VolFlow_gas_corrected: got {result['VolFlow_gas_corrected']} m3/h"
    assert result['iterations'] == expected['iterations'], f"iterations: got {result['iterations']}, expected 2"


def test_calculate_flow_wetgas_USM_VanPutten_2015_high_froude():
    """
    Test the iteration on the high Froude branch.

    An indicated flow rate is constructed backwards from the gas void fraction
    calculated outside pvtlib, so that the correct solution is known: the
    corrected flow rate must give a gas Froude number of 2.2. This verifies the
    iteration, not the accuracy of the model against measurements.
    """
    # TODO: Quality Check. Equation 29 reference from Decimal arithmetic.
    expected = {
        'Fr_gas': 2.2,  # [-]
        'alpha_gas': 0.8652780488576132,  # [-]
    }
    D = 0.2  # Inner pipe diameter [m]
    rho_g = 16.0  # Gas density [kg/m3]
    rho_l = 1521.0  # Liquid density [kg/m3]

    # Superficial gas velocity that gives Fr_gas = 2.2, from equation 7
    velocity = expected['Fr_gas'] * sqrt(9.80665 * D) * sqrt((rho_l - rho_g) / rho_g)
    VolFlow_gas_actual = velocity * (pi * D**2 / 4) * 3600  # [m3/h]

    result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        VolFlow_gas_measured=VolFlow_gas_actual / expected['alpha_gas'],  # [m3/h]
        D=D,
        rho_g=rho_g,
        rho_l=rho_l,
        GVF=0.975,  # [-]
        check_input=True
    )

    assert np.isclose(result['VolFlow_gas_corrected'], VolFlow_gas_actual, rtol=2e-10), \
        f"VolFlow_gas_corrected: got {result['VolFlow_gas_corrected']}, expected {VolFlow_gas_actual} m3/h"
    assert np.isclose(result['Fr_gas'], expected['Fr_gas'], rtol=2e-10), \
        f"Fr_gas: got {result['Fr_gas']}, expected {expected['Fr_gas']}"
    assert np.isclose(result['alpha_gas'], expected['alpha_gas'], rtol=2e-10), \
        f"alpha_gas: got {result['alpha_gas']}, expected {expected['alpha_gas']}"


def test_calculate_flow_wetgas_USM_VanPutten_2015_result_consistency():
    """
    Test that the returned results are internally consistent, at three flow
    rates and with both critical Froude number alternatives.

    Checks that the reported keys are complete and finite, that the corrected
    flow rate solves the equation it is the solution of, and that the phase flow
    rates, over-read, fractions and Froude number are consistent with each other.
    These are consistency checks, not independent numerical reference values.
    """
    cases = {
        '100 m3/h, WLR correlation': {  # TODO: Quality Check
            'VolFlow_gas_measured': 100.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': None,  # Calculate from WLR
        },
        '100 m3/h, supplied critical Froude': {  # TODO: Quality Check
            'VolFlow_gas_measured': 100.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': 1.8542921112637038,  # [-]
        },
        '1000 m3/h, WLR correlation': {  # TODO: Quality Check
            'VolFlow_gas_measured': 1000.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': None,
        },
        '1000 m3/h, supplied critical Froude': {  # TODO: Quality Check
            'VolFlow_gas_measured': 1000.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': 1.8542921112637038,  # [-]
        },
        '3000 m3/h, WLR correlation': {  # TODO: Quality Check
            'VolFlow_gas_measured': 3000.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': None,
        },
        '3000 m3/h, supplied critical Froude': {  # TODO: Quality Check
            'VolFlow_gas_measured': 3000.0,  # [m3/h]
            'D': 0.15,  # [m]
            'rho_g': 20.0,  # [kg/m3]
            'rho_l': 915.0,  # [kg/m3]
            'GVF': 0.99,  # [-]
            'WLR': 0.5,  # [-]
            'Fr_gas_crit': 1.8542921112637038,  # [-]
        },
    }

    for name, case_input in cases.items():
        result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
            **case_input, check_input=True)

        VolFlow_gas_measured = case_input['VolFlow_gas_measured']
        VolFlow_gas_corrected = result['VolFlow_gas_corrected']

        # The gas void fraction the corrected flow rate must be consistent with
        alpha_recalculated = ultrasonic_flowmeters.gas_void_fraction_VanPutten_2015(
            X=result['LockhartMartinelli'],
            Fr_gas=result['Fr_gas'],
            GVF=result['GVF'],
            Fr_gas_crit=result['Fr_gas_crit']
        )

        # The gas Froude number at the corrected flow rate
        Fr_gas_recalculated = fluid_mechanics.densimetric_froude_number(
            v=fluid_mechanics.superficial_velocity(Q_phase=VolFlow_gas_corrected, D=case_input['D']),
            D=case_input['D'],
            rho_phase=case_input['rho_g'],
            rho_other=case_input['rho_l']
        )

        assert set(result) == NUMERICAL_KEYS | DIAGNOSTIC_KEYS, \
            f'{name}: unexpected result keys {sorted(set(result))}'
        assert result['error'] is None, f"{name}: unexpected error {result['error']}"
        assert 1 <= result['iterations'] <= 100, f"{name}: iterations {result['iterations']}"
        assert all(np.isfinite(result[key]) for key in NUMERICAL_KEYS), \
            f'{name}: non-finite value in {result}'
        assert np.isclose(VolFlow_gas_corrected, VolFlow_gas_measured * alpha_recalculated, rtol=1e-10), \
            f'{name}: corrected flow rate is not the solution of the void fraction equation'
        assert np.isclose(result['Fr_gas'], Fr_gas_recalculated, rtol=1e-13), \
            f"{name}: Fr_gas {result['Fr_gas']} does not match the corrected flow rate"
        assert np.isclose(result['alpha_gas'], 1 / result['OverRead'], rtol=1e-13), \
            f'{name}: over-read is not the inverse of the gas void fraction'
        assert np.isclose(VolFlow_gas_corrected, VolFlow_gas_measured / result['OverRead'], rtol=1e-13), \
            f'{name}: corrected flow rate does not match the over-read'
        assert np.isclose(VolFlow_gas_corrected + result['VolFlow_liq'], result['VolFlow_tot']), \
            f'{name}: phase volume flow rates do not sum to the total'
        assert np.isclose(VolFlow_gas_corrected / result['VolFlow_tot'], result['GVF']), \
            f'{name}: volume flow rates are not consistent with GVF'
        assert np.isclose(result['MassFlow_gas'], VolFlow_gas_corrected * case_input['rho_g']), \
            f'{name}: gas mass flow rate does not match the gas density'
        assert np.isclose(result['MassFlow_liq'], result['VolFlow_liq'] * case_input['rho_l']), \
            f'{name}: liquid mass flow rate does not match the liquid density'
        assert np.isclose(result['GMF'], result['MassFlow_gas'] / (result['MassFlow_gas'] + result['MassFlow_liq'])), \
            f'{name}: mass flow rates are not consistent with GMF'


def test_calculate_flow_wetgas_USM_VanPutten_2015_dry_gas():
    """
    Test that the over-reading correction leaves dry-gas flow unchanged.

    Dry gas must return the indicated flow rate unchanged, with no liquid.
    """
    # TODO: Quality Check
    dry_input = {
        'VolFlow_gas_measured': 1000.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 20.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 1.0,  # [-]
        'WLR': 0.5,  # [-]
    }
    expected = {
        'VolFlow_gas_corrected': 1000.0,  # [m3/h]
        'LockhartMartinelli': 0.0,  # [-]
        'VolFlow_liq': 0.0,  # [m3/h]
        'MassFlow_liq': 0.0,  # [kg/h]
        'alpha_gas': 1.0,  # [-]
        'OverRead': 1.0,  # [-]
        'GMF': 1.0,  # [-]
    }
    dry = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**dry_input, check_input=True)

    for key, expected_value in expected.items():
        assert dry[key] == expected_value, f"Dry gas, {key}: got {dry[key]}, expected {expected_value}"


def test_calculate_flow_wetgas_USM_VanPutten_2015_zero_flow():
    """Check zero phase flows and an out-of-range Froude flag at zero indicated flow."""
    # TODO: Quality Check
    zero_input = {
        'VolFlow_gas_measured': 0.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 20.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 0.99,  # [-]
        'WLR': 0.5,  # [-]
    }
    expected = {
        'VolFlow_gas_corrected': 0.0,  # [m3/h]
        'VolFlow_liq': 0.0,  # [m3/h]
        'Fr_gas': 0.0,  # [-]
        'iterations': 1,
        'within_JIP_envelope': False,
        'JIP_envelope_exceeded': ('Fr_gas',),
    }
    zero = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**zero_input, check_input=True)

    for key in ['VolFlow_gas_corrected', 'VolFlow_liq', 'Fr_gas', 'iterations']:
        assert zero[key] == expected[key], f"Zero flow, {key}: got {zero[key]}, expected {expected[key]}"
    assert zero['within_JIP_envelope'] is False, 'Zero flow: Froude number is outside the tested range'
    assert zero['JIP_envelope_exceeded'] == expected['JIP_envelope_exceeded'], \
        f"Zero flow: got {zero['JIP_envelope_exceeded']}, expected only Fr_gas"


def test_calculate_flow_wetgas_USM_VanPutten_2015_gas_fraction_and_critical_froude_selection():
    """
    Test the input selection rules.

    GVF and GMF must describe the same condition, GVF takes precedence when both
    are supplied, and a supplied critical Froude number must replace the value
    otherwise calculated from the WLR.
    """
    # TODO: Quality Check. These compare selection rules, not an independent flow reference.
    volume_fraction_input = {
        'VolFlow_gas_measured': 1000.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 20.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 0.99,  # [-]
        'WLR': 0.5,  # [-]
    }
    from_GVF = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        **volume_fraction_input, check_input=True)

    mass_fraction_input = dict(volume_fraction_input)
    mass_fraction_input['GVF'] = None
    mass_fraction_input['GMF'] = from_GVF['GMF']
    from_GMF = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        **mass_fraction_input, check_input=True)

    both_fractions = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        **volume_fraction_input, GMF=0.5, check_input=True)

    # The WLR is not used when a critical Froude number is supplied
    Fr_gas_crit_supplied = 1.8542921112637038  # [-]
    override_input = dict(volume_fraction_input)
    override_input['WLR'] = np.nan
    override = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(
        **override_input, Fr_gas_crit=Fr_gas_crit_supplied, check_input=True)

    assert np.isclose(from_GMF['VolFlow_gas_corrected'], from_GVF['VolFlow_gas_corrected'], rtol=1e-12), \
        f"GMF input gave {from_GMF['VolFlow_gas_corrected']} m3/h, GVF input gave {from_GVF['VolFlow_gas_corrected']} m3/h"
    assert both_fractions == from_GVF, 'GVF should take precedence when both GVF and GMF are supplied'
    assert override['Fr_gas_crit'] == Fr_gas_crit_supplied, \
        f"Supplied critical Froude number was not used, got {override['Fr_gas_crit']}"
    assert override['VolFlow_gas_corrected'] != from_GVF['VolFlow_gas_corrected'], \
        'The two critical Froude numbers should give different corrected flow rates for this case'


def test_calculate_flow_wetgas_USM_VanPutten_2015_invalid_inputs():
    """
    Test invalid input handling for the flow calculation.

    All numerical results must be nan and the error must be described, with
    check_input=False. The same input must raise ValueError with check_input=True.
    Each case replaces the named inputs in the valid input set shown below.
    """
    valid_input = {
        'VolFlow_gas_measured': 1000.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 20.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 0.99,  # [-]
        'WLR': 0.5,  # [-]
    }
    cases = {
        'Negative indicated flow rate': {'VolFlow_gas_measured': -1.0},  # TODO: Quality Check
        'Zero diameter': {'D': 0.0},  # TODO: Quality Check
        'Zero gas density': {'rho_g': 0.0},  # TODO: Quality Check
        'Liquid density equal to gas density': {'rho_l': 20.0},  # TODO: Quality Check
        'Liquid density below gas density': {'rho_l': 10.0},  # TODO: Quality Check
        'Neither GVF nor GMF': {'GVF': None},  # TODO: Quality Check
        'Zero GVF': {'GVF': 0.0},  # TODO: Quality Check
        'GVF above one': {'GVF': 1.1},  # TODO: Quality Check
        'Zero GMF': {'GVF': None, 'GMF': 0.0},  # TODO: Quality Check
        'GMF above one': {'GVF': None, 'GMF': 1.1},  # TODO: Quality Check
        'Negative WLR': {'WLR': -0.1},  # TODO: Quality Check
        'WLR above one': {'WLR': 1.1},  # TODO: Quality Check
        'Zero critical Froude number': {'Fr_gas_crit': 0.0},  # TODO: Quality Check
        'Negative critical Froude number': {'Fr_gas_crit': -1.0},  # TODO: Quality Check
    }

    # TODO: Quality Check for each non-finite input.
    for argument in ['VolFlow_gas_measured', 'D', 'rho_g', 'rho_l', 'GVF', 'WLR', 'Fr_gas_crit']:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            cases[f'{argument} = {nonfinite}'] = {argument: nonfinite}
    for nonfinite in [np.nan, np.inf, -np.inf]:
        cases[f'GMF = {nonfinite}'] = {'GVF': None, 'GMF': nonfinite}

    for name, invalid_values in cases.items():
        case_input = dict(valid_input)
        case_input.update(invalid_values)

        result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input)

        assert result['error'], f'{name}: expected an error description'
        assert all(np.isnan(result[key]) for key in NUMERICAL_KEYS), \
            f'{name}: expected all numerical results to be nan, got {result}'
        assert result['within_JIP_envelope'] is False, f'{name}: expected within_JIP_envelope to be False'
        assert result['JIP_envelope_exceeded'] == (), \
            f'{name}: no range assessment was made, expected an empty tuple'

        with pytest.raises(ValueError, match=re.escape(result['error'])):
            ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input, check_input=True)


def test_calculate_flow_wetgas_USM_VanPutten_2015_non_physical_void_fraction():
    """
    Test the flow calculation when the model itself gives a non-physical result.

    At GVF = 0.5 the liquid loading is far outside the validity of equation 30,
    which then predicts a gas void fraction above 1.
    """
    # TODO: Quality Check. Expected: NaN numerical outputs and a non-physical-alpha error.
    case_input = {
        'VolFlow_gas_measured': 1000.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 20.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 0.5,  # [-]
        'WLR': 0.5,  # [-]
    }

    result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input)

    assert 'non-physical gas void fraction' in result['error'], \
        f"got error {result['error']}"
    assert all(np.isnan(result[key]) for key in NUMERICAL_KEYS), \
        f'expected all numerical results to be nan, got {result}'

    with pytest.raises(RuntimeError, match='non-physical gas void fraction'):
        ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input, check_input=True)


def test_calculate_flow_wetgas_USM_VanPutten_2015_non_finite_flow_results():
    """
    Test that non-finite derived flow rates are reported as an error.

    The densities are deliberately chosen to overflow the floating point range.
    They are not a proposed fluid.
    """
    # TODO: Quality Check. Expected: NaN numerical outputs and a non-finite-flow error.
    case_input = {
        'VolFlow_gas_measured': 1000.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 1e308,  # [kg/m3], intentionally non-physical overflow test
        'rho_l': 1.5e308,  # [kg/m3], intentionally non-physical overflow test
        'GVF': 0.99,  # [-]
        'WLR': 0.5,  # [-]
    }

    with np.errstate(over='ignore'):
        result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input)

        assert 'non-finite flow results' in result['error'], f"got error {result['error']}"
        assert all(np.isnan(result[key]) for key in NUMERICAL_KEYS), \
            f'expected all numerical results to be nan, got {result}'

        with pytest.raises(RuntimeError, match='non-finite flow results'):
            ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input, check_input=True)


def test_calculate_flow_wetgas_USM_VanPutten_2015_reports_extrapolation():
    """
    Test that a calculation outside the tested JIP ranges still returns a result,
    but reports which ranges are exceeded.

    The gas density and flow rate here give a density ratio above the tested
    range and a Froude number below it.
    """
    # TODO: Quality Check
    case_input = {
        'VolFlow_gas_measured': 10.0,  # [m3/h]
        'D': 0.15,  # [m]
        'rho_g': 50.0,  # [kg/m3]
        'rho_l': 915.0,  # [kg/m3]
        'GVF': 0.99,  # [-]
        'WLR': 0.5,  # [-]
    }
    expected = {
        'error': None,
        'within_JIP_envelope': False,
        'JIP_envelope_exceeded': ('DR', 'Fr_gas'),
    }

    result = ultrasonic_flowmeters.calculate_flow_wetgas_USM_VanPutten_2015(**case_input, check_input=True)

    assert result['error'] is None, f"unexpected error {result['error']}"
    assert result['within_JIP_envelope'] is False, 'expected within_JIP_envelope to be False'
    assert result['JIP_envelope_exceeded'] == expected['JIP_envelope_exceeded'], \
        f"got {result['JIP_envelope_exceeded']}, expected DR and Fr_gas"
