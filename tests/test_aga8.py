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

from pvtlib import AGA8
import os
import json
from pytest import raises

def test_aga8_PT():

    folder_path = os.path.join(os.path.dirname(__file__), 'data', 'aga8')
    
    #Run AGA8 setup for gerg an detail
    adapters = {
            'GERG-2008' : AGA8('GERG-2008'),
            'DETAIL' : AGA8('DETAIL')
            }
    
    tests = {}
    
    #Retrieve test data
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            
            with open(file_path, 'r') as f:
                json_string = f.read()
                test_dict = json.loads(json_string)
            
            tests[filename] = test_dict
    
    failed_tests = []       
    
    for filename, test in tests.items():
        
        equation = test['input']['equation']
        
        #excpected results from test
        test_results = test['output']
        
        results = adapters[equation].calculate_from_PT(
                    composition=test['input']['composition'], 
                    pressure=test['input']['pressure_kPa'], #KPa
                    temperature=test['input']['temperature_K'], #K
                    pressure_unit='kPa',
                    temperature_unit='K'
                    )
        
        results.pop('gas_composition')
        
        #compare calculated data against test results
        for key, value in test_results.items():
            
            if abs(value - results[key]) > 1e-10:
                failed_tests.append(f'Property: {key}, {filename}')
    
    assert failed_tests == [], f'AGA8 P&T calculation, following tests failed: {failed_tests}'


def test_aga8_rhoT():
    
    folder_path = os.path.join(os.path.dirname(__file__), 'data', 'aga8')
    
    #Run AGA8 setup for gerg an detail
    adapters = {
            'GERG-2008' : AGA8('GERG-2008'),
            'DETAIL' : AGA8('DETAIL')
            }
    
    tests = {}
    
    #Retrieve test data
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            
            with open(file_path, 'r') as f:
                json_string = f.read()
                test_dict = json.loads(json_string)
            
            tests[filename] = test_dict
    
    failed_tests = []       
    
    for filename, test in tests.items():
        
        equation = test['input']['equation']
        
        #excpected results from test
        test_results = test['output']
        
        results = adapters[equation].calculate_from_rhoT(
                    composition=test['input']['composition'], 
                    mass_density=test['output']['rho'], #mass density from test data
                    temperature=test['input']['temperature_K'],
                    temperature_unit='K'
            )
        
        results.pop('gas_composition')
        
        #compare calculated data against test results
        for key, value in test_results.items():
            
            if abs(value - results[key]) > 1e-10:
                failed_tests.append(f'Property: {key}, {filename}')
    
    assert failed_tests == [], f'AGA8 T&rho calculation, following tests failed: {failed_tests}'

def test_aga8_unit_conversion_N2():
    # Test that unit converters work properly. Use N2 at 40 bara and 20 C as test case. Use GERG-2008 equation. 
    # N2 density from NIST webbook of chemistry is used as reference.
    # The test validates that the GERG-2008 equation produces identical results as the reference density with different units of pressure and temperature, corresponding to 40 bara and 20 C

    gerg = AGA8('GERG-2008')

    # N2 composition
    composition = {'N2': 100.0}

    # Test data
    reference_density = 46.242 # kg/m3

    cases = {
        'Pa_and_K': {'pressure': 4000000, 'temperature': 293.15, 'pressure_unit': 'Pa', 'temperature_unit': 'K'},
        'psi_and_F': {'pressure': 580.1509509, 'temperature': 68.0, 'pressure_unit': 'psi', 'temperature_unit': 'F'},
        'barg_and_C': {'pressure': 38.98675, 'temperature': 20, 'pressure_unit': 'barg', 'temperature_unit': 'C'},
        'bara_and_F': {'pressure': 40, 'temperature': 68.0, 'pressure_unit': 'bara', 'temperature_unit': 'F'},
        'psig_and_F': {'pressure': 565.4550021, 'temperature': 68.0, 'pressure_unit': 'psig', 'temperature_unit': 'F'},
        'Mpa_and_C': {'pressure': 4, 'temperature': 20, 'pressure_unit': 'Mpa', 'temperature_unit': 'C'},
    }

    for case_name, case_dict in cases.items():
        results = gerg.calculate_from_PT(
            composition=composition,
            pressure=case_dict['pressure'],
            temperature=case_dict['temperature'],
            pressure_unit=case_dict['pressure_unit'],
            temperature_unit=case_dict['temperature_unit']
        )

        assert round(results['rho'],3) == reference_density, f'Failed test {case_name}'


def test_calculate_from_PH():
    
    # Run AGA8 setup for gerg and detail
    adapters = {
        'GERG-2008': AGA8('GERG-2008'),
        'DETAIL': AGA8('DETAIL')
    }
    
    # Pressure in bara, enthalpy in J/mol, temperature in C
    tests = {
        'GERG-2008': {
            'case1': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 20.0, 'enthalpy': -107.60343095444294, 'expected_temperature': 30.0},
            'case2': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 50.0, 'enthalpy': 2270.8317541569654, 'expected_temperature': 100.0},
            'case3': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 1.0, 'enthalpy': -1566.8136031983595, 'expected_temperature': -20.0},
            'case4': {'composition': {'He': 50.0, 'H2': 50.0}, 'pressure': 30.0, 'enthalpy': 161.48333628427775, 'expected_temperature': 30.0},
        },
        'DETAIL': {
            'case1': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 20.0, 'enthalpy': -107.05632228949071, 'expected_temperature': 30.0},
            'case2': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 50.0, 'enthalpy': 2273.8308175641773, 'expected_temperature': 100.0},
            'case3': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 1.0, 'enthalpy': -1566.8657354136294, 'expected_temperature': -20.0},
            'case4': {'composition': {'He': 50.0, 'H2': 50.0}, 'pressure': 30.0, 'enthalpy': 165.0220194976714, 'expected_temperature': 30.0},
        }
    }

    for equation, cases in tests.items():
        for case_name, case_dict in cases.items():
            results = adapters[equation].calculate_from_PH(
                composition=case_dict['composition'],
                pressure=case_dict['pressure'],
                enthalpy=case_dict['enthalpy'],
                pressure_unit='bara'
            )

            assert round(results['temperature'] - 273.15, 5) == case_dict['expected_temperature'], f'Failed test {case_name} with {equation}'


def test_calculate_from_PS():

    # Run AGA8 setup for gerg and detail
    adapters = {
        'GERG-2008': AGA8('GERG-2008'),
        'DETAIL': AGA8('DETAIL')
    }

    # Pressure in bara, entropy in J/(mol*K), temperature in C
    tests = {
        'GERG-2008': {
            'case1': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 20.0, 'entropy': -22.2091149233982, 'expected_temperature': 30.0},
            'case2': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 50.0, 'entropy': -22.570507319380788, 'expected_temperature': 100.0},
            'case3': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 1.0, 'entropy': -2.864966907148799, 'expected_temperature': -20.0},
            'case4': {'composition': {'He': 50.0, 'H2': 50.0}, 'pressure': 30.0, 'entropy': -22.00810645995168, 'expected_temperature': 30.0},
        },
        'DETAIL': {
            'case1': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 20.0, 'entropy': -22.207489632913457, 'expected_temperature': 30.0},
            'case2': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 50.0, 'entropy': -22.56172677087515, 'expected_temperature': 100.0},
            'case3': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 1.0, 'entropy': -2.8651449400245146, 'expected_temperature': -20.0},
            'case4': {'composition': {'He': 50.0, 'H2': 50.0}, 'pressure': 30.0, 'entropy': -21.998995602729746, 'expected_temperature': 30.0},
        }
    }

    for equation, cases in tests.items():
        for case_name, case_dict in cases.items():
            results = adapters[equation].calculate_from_PS(
                composition=case_dict['composition'],
                pressure=case_dict['pressure'],
                entropy=case_dict['entropy'],
                pressure_unit='bara'
            )

            assert round(results['temperature'] - 273.15, 5) == case_dict['expected_temperature'], f'Failed test {case_name} with {equation}'


def test_nan_inputs():
    # Test that nan inputs are handled correctly
    from math import isnan, nan

    # Test calculate_from_PT with nan pressure
    aga8 = AGA8('GERG-2008')
    composition = {'N2': 10.0, 'C1': 90.0}
    result = aga8.calculate_from_PT(composition=composition, pressure=nan, temperature=20.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PT with nan temperature
    result = aga8.calculate_from_PT(composition=composition, pressure=10.0, temperature=nan)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PT with nan in composition
    result = aga8.calculate_from_PT(composition={'N2': nan, 'C1': 90.0}, pressure=10.0, temperature=20.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_rhoT with nan mass_density
    result = aga8.calculate_from_rhoT(composition=composition, mass_density=nan, temperature=20.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_rhoT with nan temperature
    result = aga8.calculate_from_rhoT(composition=composition, mass_density=1.0, temperature=nan)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_rhoT with nan in composition
    result = aga8.calculate_from_rhoT(composition={'N2': nan, 'C1': 90.0}, mass_density=1.0, temperature=20.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PH with nan pressure
    result = aga8.calculate_from_PH(composition=composition, pressure=nan, enthalpy=100.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PH with nan enthalpy
    result = aga8.calculate_from_PH(composition=composition, pressure=10.0, enthalpy=nan)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PH with nan in composition
    result = aga8.calculate_from_PH(composition={'N2': nan, 'C1': 90.0}, pressure=10.0, enthalpy=100.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PS with nan pressure
    result = aga8.calculate_from_PS(composition=composition, pressure=nan, entropy=10.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PS with nan entropy
    result = aga8.calculate_from_PS(composition=composition, pressure=10.0, entropy=nan)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')

    # Test calculate_from_PS with nan in composition
    result = aga8.calculate_from_PS(composition={'N2': nan, 'C1': 90.0}, pressure=10.0, entropy=10.0)
    assert all(isnan(v) for k, v in result.items() if k != 'gas_composition')


def test_aga8_calculation_speed():
    """
    Test the calculation speed of the main AGA8 calculation functions.
    1000 calculations should be performed within 0.1 second.
    """
    import time
    aga8 = AGA8('GERG-2008')
    composition = {'N2': 10.0, 'C1': 90.0}

    # Test calculate_from_PT
    start = time.perf_counter()
    for _ in range(1000):
        aga8.calculate_from_PT(composition=composition, pressure=10.0, temperature=300.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1, f"calculate_from_PT is too slow: {elapsed:.3f}s for 1000 calls"

    # Test calculate_from_rhoT
    start = time.perf_counter()
    for _ in range(1000):
        aga8.calculate_from_rhoT(composition=composition, mass_density=1.0, temperature=300.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.1, f"calculate_from_rhoT is too slow: {elapsed:.3f}s for 1000 calls"

    # Test calculate_from_PH
    start = time.perf_counter()
    for _ in range(1000):
        aga8.calculate_from_PH(composition=composition, pressure=10.0, enthalpy=100.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"calculate_from_PH is too slow: {elapsed:.3f}s for 1000 calls"

    # Test calculate_from_PS
    start = time.perf_counter()
    for _ in range(1000):
        aga8.calculate_from_PS(composition=composition, pressure=10.0, entropy=10.0)
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"calculate_from_PS is too slow: {elapsed:.3f}s for 1000 calls"


def test_mix_example1():
    """Test mixing example 1: gas A (N2, C1, C2, C3) + gas D (N2, C1, C2, C3)."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_D = {'N2': 10, 'C1': 80, 'C2': 5, 'C3': 5}
    
    result = aga8.mix([gas_A, gas_D], [50, 50])
    
    # Check total mass
    assert result['total_mass'] == 100.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 5.837) < 0.01
    assert abs(result['composition']['C1'] - 85.204) < 0.01
    assert abs(result['composition']['C2'] - 5.000) < 0.01
    assert abs(result['composition']['C3'] - 3.959) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example1_mole_fractions():
    """Test mixing with mole fractions instead of mole percent (based on example 1)."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    # Same as example 1 but using mole fractions (0-1) instead of mole percent (0-100)
    gas_A = {'N2': 0.02, 'C1': 0.90, 'C2': 0.05, 'C3': 0.03}
    gas_D = {'N2': 0.10, 'C1': 0.80, 'C2': 0.05, 'C3': 0.05}
    
    result = aga8.mix([gas_A, gas_D], [50, 50])
    
    # Check total mass
    assert result['total_mass'] == 100.0
    
    # Check composition - should give same results as example 1
    assert abs(result['composition']['N2'] - 5.837) < 0.01
    assert abs(result['composition']['C1'] - 85.204) < 0.01
    assert abs(result['composition']['C2'] - 5.000) < 0.01
    assert abs(result['composition']['C3'] - 3.959) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example2():
    """Test mixing example 2: gas A (N2, C1, C2, C3) + gas B."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    
    result = aga8.mix([gas_A, gas_B], [150, 200])
    
    # Check total mass
    assert result['total_mass'] == 350.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 46.982) < 0.01
    assert abs(result['composition']['C1'] - 48.690) < 0.01
    assert abs(result['composition']['C2'] - 2.705) < 0.01
    assert abs(result['composition']['C3'] - 1.623) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example3():
    """Test mixing example 3: gas B (pure N2) + gas C (CO2, C1)."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_B = {'N2': 100}
    gas_C = {'CO2': 50, 'C1': 50}
    
    result = aga8.mix([gas_B, gas_C], [500, 600])
    
    # Check total mass
    assert result['total_mass'] == 1100.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 47.180) < 0.01
    assert abs(result['composition']['CO2'] - 26.410) < 0.01
    assert abs(result['composition']['C1'] - 26.410) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example4():
    """Test mixing example 4: gas A (N2, C1, C2, C3) + gas C (CO2, C1)."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_C = {'CO2': 50, 'C1': 50}
    
    result = aga8.mix([gas_A, gas_C], [300, 200])
    
    # Check total mass
    assert result['total_mass'] == 500.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 1.433) < 0.01
    assert abs(result['composition']['CO2'] - 14.177) < 0.01
    assert abs(result['composition']['C1'] - 78.658) < 0.01
    assert abs(result['composition']['C2'] - 3.582) < 0.01
    assert abs(result['composition']['C3'] - 2.149) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example5():
    """Test mixing example 5: Four gases - gas A, B (pure N2), C (CO2, C1), and D."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    gas_C = {'CO2': 50, 'C1': 50}
    gas_D = {'N2': 10, 'C1': 80, 'C2': 5, 'C3': 5}
    
    result = aga8.mix([gas_A, gas_B, gas_C, gas_D], [10, 20, 30, 40])
    
    # Check total mass
    assert result['total_mass'] == 100.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 21.464) < 0.01
    assert abs(result['composition']['CO2'] - 11.506) < 0.01
    assert abs(result['composition']['C1'] - 61.234) < 0.01
    assert abs(result['composition']['C2'] - 3.027) < 0.01
    assert abs(result['composition']['C3'] - 2.769) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_example6():
    """Test mixing example 6: gas A + gas E (negative mass for subtraction)."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_E = {'N2': 3, 'C1': 60, 'C2': 20, 'C3': 17}
    
    result = aga8.mix([gas_A, gas_E], [50, -10])
    
    # Check total mass
    assert result['total_mass'] == 40.0
    
    # Check composition (expected values with tolerance)
    assert abs(result['composition']['N2'] - 1.825) < 0.01
    assert abs(result['composition']['C1'] - 95.240) < 0.01
    assert abs(result['composition']['C2'] - 2.380) < 0.01
    assert abs(result['composition']['C3'] - 0.555) < 0.01
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01


def test_mix_Ar_H2():
    """Test mixing gases with H2 and Ar."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_H2 = {'H2': 100}
    gas_Ar = {'Ar': 100}
    
    result = aga8.mix([gas_H2, gas_Ar], [10, 90])
    
    # Check total mass
    assert result['total_mass'] == 100.0
    
    # Check composition sums to 100%
    total_percent = sum(result['composition'].values())
    assert abs(total_percent - 100.0) < 0.01
    
    # Should only contain H2 and Ar
    assert 'H2' in result['composition']
    assert 'Ar' in result['composition']
    assert len(result['composition']) == 2
    
    # Check expected mol% with tolerance
    assert abs(result['composition']['H2'] - 68.767) < 0.01
    assert abs(result['composition']['Ar'] - 31.233) < 0.01


def test_mix_unequal_list_lengths_error():
    """Test that error is raised when compositions and mix_weights have different lengths."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    gas_C = {'CO2': 50, 'C1': 50}
    
    # Provide 3 compositions but only 2 masses - should raise error with check_input=True
    with raises(ValueError, match='Length of compositions and mix_weights'):
        aga8.mix([gas_A, gas_B, gas_C], [100, 50], check_input=True)


def test_mix_unequal_list_lengths_nan():
    """Test that NaN is returned when compositions and mix_weights have different lengths with check_input=False."""
    from pvtlib import AGA8
    import numpy as np
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    
    # Provide 2 compositions but only 1 mass - should return NaN with check_input=False
    result = aga8.mix([gas_A, gas_B], [100], check_input=False)
    
    assert np.isnan(result['total_mass'])
    assert all(np.isnan(v) for v in result['composition'].values())


def test_mix_excessive_subtraction_error():
    """Test that error is raised when subtraction results in negative components."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_E = {'N2': 3, 'C1': 60, 'C2': 20, 'C3': 17}
    
    # Subtract too much (60 kg instead of 10 kg) - should cause negative components
    with raises(ValueError, match='Negative moles'):
        aga8.mix([gas_A, gas_E], [50, -60], check_input=True)


def test_mix_excessive_subtraction_nan():
    """Test that NaN is returned when subtraction results in negative components with check_input=False."""
    from pvtlib import AGA8
    import numpy as np
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_E = {'N2': 3, 'C1': 60, 'C2': 20, 'C3': 17}
    
    # Subtract too much - should return NaN with check_input=False
    result = aga8.mix([gas_A, gas_E], [50, -60], check_input=False)
    
    assert np.isnan(result['total_mass'])
    assert all(np.isnan(v) for v in result['composition'].values())


def test_mix_negative_total_mass_error():
    """Test that error is raised when total mass becomes negative."""
    from pvtlib import AGA8
    
    aga8 = AGA8('GERG-2008')
    
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    
    # Subtract more mass than available - will trigger negative moles or negative mass error
    with raises(ValueError):
        aga8.mix([gas_A, gas_B], [50, -100], check_input=True)


def test_mix_performance():
    """Test mix function performance by running 1000 iterations."""
    from pvtlib import AGA8
    import time
    
    aga8 = AGA8('GERG-2008')
    
    # Use a mix of different complexities
    gas_A = {'N2': 2, 'C1': 90, 'C2': 5, 'C3': 3}
    gas_B = {'N2': 100}
    gas_C = {'CO2': 50, 'C1': 50}
    gas_D = {'N2': 10, 'C1': 80, 'C2': 5, 'C3': 5}
    
    # Warm up (ensure AGA8 is fully initialized)
    _ = aga8.mix([gas_A, gas_D], [50, 50])
    
    # Time 1000 iterations
    n_iterations = 1000
    start_time = time.perf_counter()
    
    for _ in range(n_iterations):
        result = aga8.mix([gas_A, gas_D], [50, 50])
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    avg_time_ms = (elapsed_time / n_iterations) * 1000
    
    # Print timing results
    print(f"\n{n_iterations} mix operations completed in {elapsed_time:.3f} seconds")
    print(f"Average time per mix: {avg_time_ms:.3f} ms")
    
    # Assert reasonable performance (should be very fast with numpy vectorization)
    assert avg_time_ms < 1.0, f"Mix operation too slow: {avg_time_ms:.3f} ms per operation"


def test_gerg_gas1_properties():
    """Test GERG-2008 calculation for Gas 1 composition against expected reference values."""
    from pvtlib import AGA8
    
    # Initialize GERG-2008
    gerg = AGA8('GERG-2008')
    
    # Gas 1 composition and conditions
    composition = {
        'N2': 1,
        'CO2': 2,
        'C1': 90,
        'C2': 6,
        'C3': 0.9,
        'iC4': 0.05,
        'nC4': 0.05
    }
    
    pressure = 150  # bara
    temperature = 50  # °C
    
    # Calculate properties
    result = gerg.calculate_from_PT(
        composition=composition,
        pressure=pressure,
        temperature=temperature,
        pressure_unit='bara',
        temperature_unit='C'
    )
    
    # Expected values (reference from other software)
    expected = {
        'rho': 118.40011648,      # Density [kg/m³]
        'w': 457.29319197,        # Speed of sound [m/s]
        'mm': 17.85766318,        # Molar mass [g/mol]
        'z': 0.84202487,          # Compressibility factor [-]
        'kappa': 1.65063231,      # Isentropic exponent [-]
        'cp': 55.12684554,        # Isobaric heat capacity [J/(mol·K)]
        'cv': 31.96913688         # Isochoric heat capacity [J/(mol·K)]
    }
    
    # Verify results with appropriate tolerance
    # Use relative tolerance for better precision across different magnitudes
    relative_tolerance = 1e-6  # 0.0001% relative error
    
    print("\nGERG-2008 Properties for Gas 1:")
    print(f"{'Property':<20} {'Calculated':<15} {'Expected':<15} {'Match':<10}")
    print("-" * 60)
    
    for prop, expected_value in expected.items():
        calculated_value = result[prop]
        relative_error = abs((calculated_value - expected_value) / expected_value)
        matches = relative_error < relative_tolerance
        status = "✓" if matches else "✗"
        print(f"{prop:<20} {calculated_value:<15.8f} {expected_value:<15.8f} {status:<10}")
        
        assert relative_error < relative_tolerance, \
            f"{prop}: calculated {calculated_value:.8f}, expected {expected_value:.8f}, relative error {relative_error:.2e}"

