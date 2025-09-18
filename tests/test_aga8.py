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
            
            if abs(value - results[key]) > 1e-20:
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
