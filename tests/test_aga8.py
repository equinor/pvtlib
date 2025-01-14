from pvtlib import aga8
import os
import json

def test_aga8_P_T():

    folder_path = r'tests\data\aga8'
    
    #Run AGA8 setup for gerg an detail
    adapters = {
            'GERG-2008' : aga8('GERG-2008'),
            'DETAIL' : aga8('DETAIL')
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
        
        results = adapters[equation].calculate_from_P_T(
                    composition=test['input']['composition'], 
                    pressure=test['input']['pressure_kPa'], #KPa
                    temperature=test['input']['temperature_K'] #K
                    )
        
        results.pop('gas_composition')
        
        #compare calculated data against test results
        for key, value in test_results.items():
            
            if abs(value - results[key]) > 1e-20:
                failed_tests.append(f'Property: {key}, {filename}')
    
    assert failed_tests == [], f'AGA8 P&T calculation, following tests failed: {failed_tests}'


def test_aga8_T_rho():
    
    folder_path = r'tests\data\aga8'
    
    #Run AGA8 setup for gerg an detail
    adapters = {
            'GERG-2008' : aga8('GERG-2008'),
            'DETAIL' : aga8('DETAIL')
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
        
        results = adapters[equation].calculate_from_T_and_rho(
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