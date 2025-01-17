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
