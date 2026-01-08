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

from pvtlib import thermodynamics, utilities
import numpy as np

def test_natural_gas_viscosity_Lee_et_al():

    # Test data against experimental data from Lee, A.L., M.H. Gonzalez, and B.E. Eakin, The Viscosity of Natural Gases. Journal of Petroleum Technology, 1966 

    cases={ 
        # case1, case2 and case3 are from the paper (sample 4) where mu_expected is the experimental value of viscosity (mu_E). Use a accept criteria of 10% for these
        # however, I was not able to reproduce the calculated values (mu_c) from the paper. Could be an error in the paper..?
        'case1':{'T':171.11,'M':18.26,'rho':105.6,'mu_expected':0.01990 , 'criteria':10.0}, # 3000 psi and 340 F
        'case2':{'T':37.78,'M':18.26,'rho':310.6,'mu_expected':0.04074, 'criteria':10.0}, # 8000 psi and 100 F 309.13 g/cc
        'case3':{'T':137.78,'M':18.26,'rho':15.1,'mu_expected':0.01602, 'criteria':10.0}, # 400 psi and 280 F
        
        # case4 is from calculation example at https://petrowiki.spe.org/Gas_viscosity. This is reproduced identically. 
        'case4':{'T':65.55,'M':20.079,'rho':110.25,'mu_expected':0.01625, 'criteria':0.1}, # 60 F, 0.7 g/cc
    }


    for case_name, case_dict in cases.items():
        mu=thermodynamics.natural_gas_viscosity_Lee_et_al(
            T=case_dict['T'],
            M=case_dict['M'],
            rho=case_dict['rho']
        )

        # Calculate relative error
        relative_error=abs(utilities.calculate_relative_deviation(mu,case_dict['mu_expected']))
        
        assert relative_error<case_dict['criteria'], f'Natural gas viscosity calculation failed for {case_name}'


def test_density_from_sos_kappa():
    """
    Test density_from_sos_kappa function based on GFMW2024 paper.
    
    Reference case:
    - Pressure: 100 bara
    - Temperature: 50 C
    - Properties from GERG-2008:
      - rho: 75.9810 kg/m3
      - sos: 434.0811 m/s
      - M: 17.8016 kg/kmol
      - Z: 0.8720
      - kappa: 1.4317 (calculated from GERG-2008)
    
    When measured speed of sound is 433 m/s, expected density is 76.361 kg/m3
    """
    # Input values
    measured_sos = 433.0  # m/s
    kappa = 1.4317  # From GERG-2008
    pressure_bara = 100.0  # bara
    
    # Expected result from GFMW2024 paper
    expected_rho = 76.361  # kg/m3
    
    # Calculate density
    calculated_rho = thermodynamics.density_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa,
        pressure_bara=pressure_bara
    )
    
    # Calculate relative error (tolerance: 0.1%)
    relative_error = abs(utilities.calculate_relative_deviation(calculated_rho, expected_rho))
    
    assert relative_error < 0.01, f'Density from speed of sound calculation failed. Expected: {expected_rho:.3f}, Got: {calculated_rho:.3f}, Error: {relative_error:.2f}%'


def test_sos_from_rho_kappa():
    """
    Test sos_from_rho_kappa function based on GFMW2024 paper.
    
    Reference case:
    - Pressure: 100 bara
    - Temperature: 50 C
    - Properties from GERG-2008:
      - rho: 75.9810 kg/m3
      - sos: 434.0811 m/s
      - M: 17.8016 kg/kmol
      - Z: 0.8720
      - kappa: 1.4317 (calculated from GERG-2008)
    
    When measured density is 75 kg/m3, expected speed of sound is 436.91 m/s
    """
    # Input values
    measured_rho = 75.0  # kg/m3
    kappa = 1.4317  # From GERG-2008
    pressure_bara = 100.0  # bara
    
    # Expected result from GFMW2024 paper
    expected_sos = 436.91  # m/s
    
    # Calculate speed of sound
    calculated_sos = thermodynamics.sos_from_rho_kappa(
        measured_rho=measured_rho,
        kappa=kappa,
        pressure_bara=pressure_bara
    )
    
    # Calculate relative error (tolerance: 0.1%)
    relative_error = abs(utilities.calculate_relative_deviation(calculated_sos, expected_sos))
    
    assert relative_error < 0.01, f'Speed of sound from density calculation failed. Expected: {expected_sos:.2f}, Got: {calculated_sos:.2f}, Error: {relative_error:.2f}%'


def test_molar_mass_from_sos_kappa():
    """
    Test molar_mass_from_sos_kappa function based on GFMW2024 paper.
    
    Reference case:
    - Pressure: 100 bara
    - Temperature: 50 C
    - Properties from GERG-2008:
      - rho: 75.9810 kg/m3
      - sos: 434.0811 m/s
      - M: 17.8016 kg/kmol
      - Z: 0.8720
      - kappa: 1.4317 (calculated from GERG-2008)
    
    When measured speed of sound is 433 m/s, expected molar mass is 17.891 g/mol (17.891 kg/kmol)
    """
    # Input values
    measured_sos = 433.0  # m/s
    kappa = 1.4317  # From GERG-2008
    Z = 0.8720  # From GERG-2008
    temperature_C = 50.0  # C
    
    # Expected result from GFMW2024 paper
    expected_M = 17.891  # kg/kmol (same as g/mol)
    
    # Calculate molar mass
    calculated_M = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa,
        Z=Z,
        temperature_C=temperature_C
    )
    
    # Calculate relative error (tolerance: 0.1%)
    relative_error = abs(utilities.calculate_relative_deviation(calculated_M, expected_M))
    
    assert relative_error < 0.01, f'Molar mass from speed of sound calculation failed. Expected: {expected_M:.3f}, Got: {calculated_M:.3f}, Error: {relative_error:.2f}%'


def test_Z_from_sos_kappa():
    """
    Test Z_from_sos_kappa function based on GFMW2024 paper.
    
    Reference case:
    - Pressure: 100 bara
    - Temperature: 50 C
    - Properties from GERG-2008:
      - rho: 75.9810 kg/m3
      - sos: 434.0811 m/s
      - M: 17.8016 kg/kmol
      - Z: 0.8720
      - kappa: 1.4317 (calculated from GERG-2008)
    
    When measured speed of sound is 433 m/s, expected compressibility factor Z is 0.8677
    """
    # Input values
    measured_sos = 433.0  # m/s
    kappa = 1.4317  # From GERG-2008
    molar_mass = 17.8016  # kg/kmol (from GERG-2008)
    temperature_C = 50.0  # C
    
    # Expected result from GFMW2024 paper
    expected_Z = 0.8677
    
    # Calculate compressibility factor
    calculated_Z = thermodynamics.Z_from_sos_kappa(
        measured_sos=measured_sos,
        kappa=kappa,
        molar_mass=molar_mass,
        temperature_C=temperature_C
    )
    
    # Calculate relative error (tolerance: 0.1%)
    relative_error = abs(utilities.calculate_relative_deviation(calculated_Z, expected_Z))
    
    assert relative_error < 0.01, f'Compressibility factor from speed of sound calculation failed. Expected: {expected_Z:.4f}, Got: {calculated_Z:.4f}, Error: {relative_error:.2f}%'


def test_density_from_sos_kappa_invalid_inputs():
    """
    Test density_from_sos_kappa function with invalid inputs.
    
    Tests:
    1. Zero speed of sound should return NaN
    2. Negative speed of sound should still calculate (mathematically valid but physically meaningless)
    3. Zero kappa should return zero density
    4. Zero pressure should return zero density
    """
    import numpy as np
    
    # Test 1: Zero speed of sound should return NaN
    result = thermodynamics.density_from_sos_kappa(
        measured_sos=0.0,
        kappa=1.4317,
        pressure_bara=100.0
    )
    assert np.isnan(result), f'Expected NaN for zero speed of sound, got {result}'
    
    # Test 2: Negative speed of sound (squared in formula, so still produces result)
    result = thermodynamics.density_from_sos_kappa(
        measured_sos=-433.0,
        kappa=1.4317,
        pressure_bara=100.0
    )
    assert not np.isnan(result) and result > 0, f'Negative speed of sound should still produce positive density due to squaring'
    
    # Test 3: Zero kappa should return zero density
    result = thermodynamics.density_from_sos_kappa(
        measured_sos=433.0,
        kappa=0.0,
        pressure_bara=100.0
    )
    assert result == 0.0, f'Expected 0 for zero kappa, got {result}'
    
    # Test 4: Zero pressure should return zero density
    result = thermodynamics.density_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        pressure_bara=0.0
    )
    assert result == 0.0, f'Expected 0 for zero pressure, got {result}'


def test_sos_from_rho_kappa_invalid_inputs():
    """
    Test sos_from_rho_kappa function with invalid inputs.
    
    Tests:
    1. Zero density should return NaN
    2. Negative density should return NaN (would cause sqrt of negative)
    3. Zero kappa with zero pressure should return NaN
    4. Negative kappa should return NaN (would cause sqrt of negative)
    """
    import numpy as np
    
    # Test 1: Zero density should return NaN
    result = thermodynamics.sos_from_rho_kappa(
        measured_rho=0.0,
        kappa=1.4317,
        pressure_bara=100.0
    )
    assert np.isnan(result), f'Expected NaN for zero density, got {result}'
    
    # Test 2: Negative density should return NaN
    result = thermodynamics.sos_from_rho_kappa(
        measured_rho=-75.0,
        kappa=1.4317,
        pressure_bara=100.0
    )
    assert np.isnan(result), f'Expected NaN for negative density, got {result}'
    
    # Test 3: Zero kappa with zero pressure should return NaN (0/0)
    result = thermodynamics.sos_from_rho_kappa(
        measured_rho=75.0,
        kappa=0.0,
        pressure_bara=0.0
    )
    assert np.isnan(result) or result == 0.0, f'Expected NaN or 0 for zero kappa and zero pressure, got {result}'
    
    # Test 4: Negative kappa should return NaN (sqrt of negative if pressure positive)
    result = thermodynamics.sos_from_rho_kappa(
        measured_rho=75.0,
        kappa=-1.4317,
        pressure_bara=100.0
    )
    assert np.isnan(result), f'Expected NaN for negative kappa, got {result}'


def test_molar_mass_from_sos_kappa_invalid_inputs():
    """
    Test molar_mass_from_sos_kappa function with invalid inputs.
    
    Tests:
    1. Zero speed of sound should return NaN
    2. Zero kappa should return zero molar mass
    3. Zero Z should return zero molar mass
    4. Very low temperature (near absolute zero) should still calculate
    5. Negative speed of sound (squared in formula)
    """

    
    # Test 1: Zero speed of sound should return NaN
    result = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=0.0,
        kappa=1.4317,
        Z=0.8720,
        temperature_C=50.0
    )
    assert np.isnan(result), f'Expected NaN for zero speed of sound, got {result}'
    
    # Test 2: Zero kappa should return zero molar mass
    result = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=433.0,
        kappa=0.0,
        Z=0.8720,
        temperature_C=50.0
    )
    assert result == 0.0, f'Expected 0 for zero kappa, got {result}'
    
    # Test 3: Zero Z should return zero molar mass
    result = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        Z=0.0,
        temperature_C=50.0
    )
    assert result == 0.0, f'Expected 0 for zero Z, got {result}'
    
    # Test 4: Very low temperature (near absolute zero, -273 C)
    result = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        Z=0.8720,
        temperature_C=-273.0
    )
    assert result >= 0 and result < 0.1, f'Expected near-zero molar mass for near absolute zero temperature, got {result}'
    
    # Test 5: Negative speed of sound (squared in formula, so still produces result)
    result = thermodynamics.molar_mass_from_sos_kappa(
        measured_sos=-433.0,
        kappa=1.4317,
        Z=0.8720,
        temperature_C=50.0
    )
    assert not np.isnan(result) and result > 0, f'Negative speed of sound should still produce positive molar mass due to squaring'


def test_Z_from_sos_kappa_invalid_inputs():
    """
    Test Z_from_sos_kappa function with invalid inputs.
    
    Tests:
    1. Zero kappa should return NaN
    2. Zero R (gas constant) should return NaN
    3. Temperature at absolute zero (-273.15 C) should return NaN
    4. Zero molar mass should return zero Z
    5. Zero speed of sound should return zero Z
    """
    import numpy as np
    
    # Test 1: Zero kappa should return NaN
    result = thermodynamics.Z_from_sos_kappa(
        measured_sos=433.0,
        kappa=0.0,
        molar_mass=17.8016,
        temperature_C=50.0
    )
    assert np.isnan(result), f'Expected NaN for zero kappa, got {result}'
    
    # Test 2: Zero R (gas constant) should return NaN
    result = thermodynamics.Z_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        molar_mass=17.8016,
        temperature_C=50.0,
        R=0.0
    )
    assert np.isnan(result), f'Expected NaN for zero R, got {result}'
    
    # Test 3: Temperature at absolute zero should return NaN
    result = thermodynamics.Z_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        molar_mass=17.8016,
        temperature_C=-273.15
    )
    assert np.isnan(result), f'Expected NaN for absolute zero temperature, got {result}'
    
    # Test 4: Zero molar mass should return zero Z
    result = thermodynamics.Z_from_sos_kappa(
        measured_sos=433.0,
        kappa=1.4317,
        molar_mass=0.0,
        temperature_C=50.0
    )
    assert result == 0.0, f'Expected 0 for zero molar mass, got {result}'
    
    # Test 5: Zero speed of sound should return zero Z
    result = thermodynamics.Z_from_sos_kappa(
        measured_sos=0.0,
        kappa=1.4317,
        molar_mass=17.8016,
        temperature_C=50.0
    )
    assert result == 0.0, f'Expected 0 for zero speed of sound, got {result}'


        



        

