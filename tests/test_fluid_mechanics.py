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

from pvtlib import fluid_mechanics
import numpy as np


def test_mixture_density_homogeneous_cases():
    """
    Test mixture_density_homogeneous function with multiple cases.
    """
    cases = [
        # (volume_fractions, densities, expected)
        {"volume_fractions": [0.5, 0.5], "densities": [1000, 800], "expected": 900.0},
        {"volume_fractions": [1, 0], "densities": [1000, 800], "expected": 1000.0},
        {"volume_fractions": [0, 1], "densities": [1000, 800], "expected": 800.0},
        {"volume_fractions": [2, 1], "densities": [900, 600], "expected": 800.0},
        {"volume_fractions": [0.2, 0.8], "densities": [1000, 800], "expected": 840.0},
        {"volume_fractions": [0, 0], "densities": [1000, 800], "expected": np.nan},
        {"volume_fractions": [1, 1], "densities": [0, 800], "expected": np.nan},
        {"volume_fractions": [1, 1], "densities": [1000, -800], "expected": np.nan},
        {"volume_fractions": [-1, 2], "densities": [1000, 800], "expected": np.nan},
        {"volume_fractions": [1, 1], "densities": [np.nan, 800], "expected": np.nan},
        {"volume_fractions": [1, 1], "densities": [1000, np.nan], "expected": np.nan},
        {"volume_fractions": [1, 1, 1], "densities": [1000, 800, 600], "expected": 800.0},
        {"volume_fractions": [0, 0, 0], "densities": [1000, 800, 600], "expected": np.nan},
        {"volume_fractions": [0, 1, 1], "densities": [np.nan, 800, 600], "expected": 700.0},
    ]
    for case in cases:
        try:
            result = fluid_mechanics.mixture_density_homogeneous(case["volume_fractions"], case["densities"])
        except ValueError:
            # If ValueError is expected (e.g., mismatched lengths), expected must be ValueError
            assert case.get("expected") == ValueError, f"mixture_density_homogeneous failed for {case}"
            continue
        if isinstance(case["expected"], float) and np.isnan(case["expected"]):
            assert np.isnan(result), f"mixture_density_homogeneous failed for {case}: {result} != {case['expected']}"
        else:
            assert np.isclose(result, case["expected"]), f"mixture_density_homogeneous failed for {case}: {result} != {case['expected']}"


def test_mixture_density_homogeneous_shape_mismatch():
    """
    Test mixture_density_homogeneous raises ValueError for mismatched input lengths.
    """
    try:
        fluid_mechanics.mixture_density_homogeneous([1, 2], [1000])
    except ValueError:
        pass
    else:
        assert False, "mixture_density_homogeneous should raise ValueError for mismatched input lengths"

def test_GMF_to_GVF_cases():
    """
    Test GMF_to_GVF function with multiple cases.
    """
    cases = [
        # (GMF, rho_gas, rho_liquid, expected_GVF)
        {"GMF": 0.5, "rho_gas": 100, "rho_liquid": 1000, "expected": 0.9090909090909091},
        {"GMF": 0.1, "rho_gas": 50, "rho_liquid": 900, "expected": 0.6666666666666666},
        {"GMF": 0.9, "rho_gas": 10, "rho_liquid": 1000, "expected": 0.998890122087},
        {"GMF": 1.0, "rho_gas": 100, "rho_liquid": 1000, "expected": 1.0},
        {"GMF": 0.0, "rho_gas": 100, "rho_liquid": 1000, "expected": 0.0},
        {"GMF": -0.1, "rho_gas": 100, "rho_liquid": 1000, "expected": np.nan},
        {"GMF": 0.5, "rho_gas": 0, "rho_liquid": 1000, "expected": np.nan},
        {"GMF": 0.5, "rho_gas": 100, "rho_liquid": 0, "expected": np.nan},
    ]
    for case in cases:
        result = fluid_mechanics.GMF_to_GVF(case["GMF"], case["rho_gas"], case["rho_liquid"])
        if np.isnan(case["expected"]):
            assert np.isnan(result), f"GMF_to_GVF failed for {case}"
        else:
            assert np.isclose(result, case["expected"]), f"GMF_to_GVF failed for {case}: {result} != {case['expected']}"


def test_GVF_to_GMF_cases():
    """
    Test GVF_to_GMF function with multiple cases.
    """
    cases = [
        # (GVF, rho_gas, rho_liquid, expected_GMF)
        {"GVF": 0.5, "rho_gas": 100, "rho_liquid": 1000, "expected": 0.09090909090909091},
        {"GVF": 0.1, "rho_gas": 50, "rho_liquid": 900, "expected": 0.006134969325153374},
        {"GVF": 0.9, "rho_gas": 10, "rho_liquid": 1000, "expected": 0.08256880733944957},
        {"GVF": 1.0, "rho_gas": 100, "rho_liquid": 1000, "expected": 1.0},
        {"GVF": 0.0, "rho_gas": 100, "rho_liquid": 1000, "expected": 0.0},
        {"GVF": -0.1, "rho_gas": 100, "rho_liquid": 1000, "expected": np.nan},
        {"GVF": 0.5, "rho_gas": 0, "rho_liquid": 1000, "expected": np.nan},
        {"GVF": 0.5, "rho_gas": 100, "rho_liquid": 0, "expected": np.nan},
    ]
    for case in cases:
        result = fluid_mechanics.GVF_to_GMF(case["GVF"], case["rho_gas"], case["rho_liquid"])
        if np.isnan(case["expected"]):
            assert np.isnan(result), f"GVF_to_GMF failed for {case}"
        else:
            assert np.isclose(result, case["expected"]), f"GVF_to_GMF failed for {case}: {result} != {case['expected']}"


#%% Test equations for evaluating homogeneous mixtures of oil and water in horizontal and vertical pipes (used in water-cut measurements)
def test_critical_velocity_for_uniform_wio_dispersion_horizontal_1():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a horizontal pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test with 5 cP (0.005 Pa⋅s)
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_horizontal(
        ST_oil_aq=0.025, 
        rho_o=800,
        rho_aq=1025, 
        Visc_o=0.005, 
        D=0.1016
        )
    
    assert round(Vc,4) == 3.7731, f'Critical velocity for homogeneous oil water mixture in a horizontal pipe failed'
    

def test_critical_velocity_for_uniform_wio_dispersion_horizontal_2():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a horizontal pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test with 20 cP (0.020 Pa⋅s)
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_horizontal(
        ST_oil_aq=0.025, 
        rho_o=800,
        rho_aq=1025, 
        Visc_o=0.020, 
        D=0.1016
        )
    
    assert round(Vc,4) == 2.0759, f'Critical velocity for homogeneous oil water mixture in a horizontal pipe failed'


def test_critical_velocity_for_uniform_wio_dispersion_horizontal_3():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a horizontal pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test if all parameters are zero, should return nan. 
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_horizontal(
        ST_oil_aq=0.0, 
        rho_o=0.0,
        rho_aq=0.0, 
        Visc_o=0.0, 
        D=0.0
        )
    
    assert np.isnan(Vc), f'Critical velocity for homogeneous oil water mixture in a horizontal pipe failed'


def test_critical_velocity_for_uniform_wio_dispersion_vertical_1():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a vertical pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test with Betha = 10 vol%
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_vertical(
        beta=10.0, 
        ST_oil_aq=0.025, 
        rho_o=800,
        rho_aq=1025, 
        Visc_o=0.005, 
        D=0.1016
        )
    
    assert round(Vc,4) == 1.1062, f'Critical velocity for homogeneous oil water mixture in a vertical pipe failed'
    
    
def test_critical_velocity_for_uniform_wio_dispersion_vertical_2():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a vertical pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test with Betha = 1 vol%
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_vertical(
        beta=1.0, 
        ST_oil_aq=0.025, 
        rho_o=800,
        rho_aq=1025, 
        Visc_o=0.005, 
        D=0.1016
        )
    
    assert round(Vc,4) == 0.2651, f'Critical velocity for homogeneous oil water mixture in a vertical pipe failed'    
    
    
def test_critical_velocity_for_uniform_wio_dispersion_vertical_3():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a vertical pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test if all parameters are zero, should return nan.
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_vertical(
        beta=100.0, 
        ST_oil_aq=0.0, 
        rho_o=0.0,
        rho_aq=0.0, 
        Visc_o=0.0, 
        D=0.0
        )
    
    assert np.isnan(Vc), f'Critical velocity for homogeneous oil water mixture in a vertical pipe failed'    

def test_critical_velocity_for_uniform_wio_dispersion_vertical_4():
    '''
    Test calculation of critical (minimum) velocity for maintaining homogeneous oil water mixture in a vertical pipe. 
    Test is based on example from NFOGM Handbook of Water Fraction Metering Revision 2, December 2004, Appendix A
    
    Test with Betha > 100 vol%, should return nan
    '''
    
    
    Vc = fluid_mechanics.critical_velocity_for_uniform_wio_dispersion_vertical(
        beta=300.0, 
        ST_oil_aq=0.025, 
        rho_o=800,
        rho_aq=1025, 
        Visc_o=0.005, 
        D=0.1016
        )
    
    assert np.isnan(Vc), f'Critical velocity for homogeneous oil water mixture in a vertical pipe failed'


# Test equations for oil-in-water and water-in-oil
def test_dominant_phase_corrected_density_1():
    '''
    Test calculation of dominant phase corrected density.
    Example: Measured density is 800 kg/m3 and the water fraction is 1 vol%.
    '''
    
    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=703,
        ContaminantVolP=1.0,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(corrected_density, 2) == 700.0, f'Dominant phase corrected density calculation failed'


def test_dominant_phase_corrected_density_2():
    '''
    Test calculation of dominant phase corrected density.
    Example: Measured density is 850 kg/m3 and the water fraction is 5 vol%.
    '''
    
    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=850,
        ContaminantVolP=5,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(corrected_density, 2) == 842.11, f'Dominant phase corrected density calculation failed'


def test_dominant_phase_corrected_density_3():
    '''
    Test calculation of dominant phase corrected density.
    Example: Measured density is 900 kg/m3 and the water fraction is 10 vol%.
    '''
    
    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=900,
        ContaminantVolP=10,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(corrected_density, 2) == 888.89, f'Dominant phase corrected density calculation failed'


def test_dominant_phase_corrected_density_all_zeros():
    '''
    Test calculation of dominant phase corrected density when all parameters are zero.
    Should return nan.
    '''
    
    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=0,
        ContaminantVolP=0.0,
        ContaminantPhase_EOS_density=0
    )
    
    assert corrected_density==0.0, f'Dominant phase corrected density calculation failed'


def test_dominant_phase_corrected_density_invalid_fraction():
    '''
    Test calculation of dominant phase corrected density when contaminant volume fraction is 100%.
    Should return nan.
    '''
    
    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=800,
        ContaminantVolP=100,
        ContaminantPhase_EOS_density=1000
    )
    
    assert np.isnan(corrected_density), f'Dominant phase corrected density calculation failed'


def test_mass_percent_to_volume_percent_1():
    '''
    Test conversion from mass percentage to volume percentage.
    Example: Mass percentage is 10%, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantVolP = fluid_mechanics.mass_percent_to_volume_percent(
        ContaminantMassP=10,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantVolP, 2) == 8.16, f'Mass to volume percentage conversion failed'


def test_mass_percent_to_volume_percent_2():
    '''
    Test conversion from mass percentage to volume percentage.
    Example: Mass percentage is 50%, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantVolP = fluid_mechanics.mass_percent_to_volume_percent(
        ContaminantMassP=50,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantVolP, 2) == 44.44, f'Mass to volume percentage conversion failed'


def test_mass_percent_to_volume_percent_all_zeros():
    '''
    Test conversion from mass percentage to volume percentage when all parameters are zero.
    Should return nan.
    '''
    
    ContaminantVolP = fluid_mechanics.mass_percent_to_volume_percent(
        ContaminantMassP=0,
        DominantPhase_EOS_density=0,
        ContaminantPhase_EOS_density=0
    )
    
    assert np.isnan(ContaminantVolP), f'Mass to volume percentage conversion failed'


def test_mass_percent_to_volume_percent_invalid_density():
    '''
    Test conversion from mass percentage to volume percentage when densities are zero.
    Should return nan.
    '''
    
    ContaminantVolP = fluid_mechanics.mass_percent_to_volume_percent(
        ContaminantMassP=10,
        DominantPhase_EOS_density=0,
        ContaminantPhase_EOS_density=0
    )
    
    assert np.isnan(ContaminantVolP), f'Mass to volume percentage conversion failed'

def test_volume_percent_to_mass_percent_1():
    '''
    Test conversion from volume percentage to mass percentage.
    Example: Volume percentage is 10%, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantMassP = fluid_mechanics.volume_percent_to_mass_percent(
        ContaminantVolP=10,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantMassP, 2) == 12.2, f'Volume to mass percentage conversion failed'


def test_volume_percent_to_mass_percent_2():
    '''
    Test conversion from volume percentage to mass percentage.
    Example: Volume percentage is 50%, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantMassP = fluid_mechanics.volume_percent_to_mass_percent(
        ContaminantVolP=50,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantMassP, 2) == 55.56, f'Volume to mass percentage conversion failed'


def test_volume_percent_to_mass_percent_all_zeros():
    '''
    Test conversion from volume percentage to mass percentage when all parameters are zero.
    Should return nan.
    '''
    
    ContaminantMassP = fluid_mechanics.volume_percent_to_mass_percent(
        ContaminantVolP=0,
        DominantPhase_EOS_density=0,
        ContaminantPhase_EOS_density=0
    )
    
    assert np.isnan(ContaminantMassP), f'Volume to mass percentage conversion failed'


def test_volume_percent_to_mass_percent_invalid_density():
    '''
    Test conversion from volume percentage to mass percentage when densities are zero.
    Should return nan.
    '''
    
    ContaminantMassP = fluid_mechanics.volume_percent_to_mass_percent(
        ContaminantVolP=10,
        DominantPhase_EOS_density=0,
        ContaminantPhase_EOS_density=0
    )
    
    assert np.isnan(ContaminantMassP), f'Volume to mass percentage conversion failed'

def test_contaminant_volume_percent_from_mixed_density_1():
    '''
    Test calculation of contaminant volume percent from mixed density.
    Example: Measured density is 850 kg/m3, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=850,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantVolP, 2) == 25.0, f'Contaminant volume percent calculation failed'


def test_contaminant_volume_percent_from_mixed_density_2():
    '''
    Test calculation of contaminant volume percent from mixed density.
    Example: Measured density is 900 kg/m3, Dominant phase density is 800 kg/m3, Contaminant phase density is 1000 kg/m3.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=900,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert round(ContaminantVolP, 2) == 50.0, f'Contaminant volume percent calculation failed'


def test_contaminant_volume_percent_from_mixed_density_all_zeros():
    '''
    Test calculation of contaminant volume percent from mixed density when all parameters are zero.
    Should return nan.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=0,
        DominantPhase_EOS_density=0,
        ContaminantPhase_EOS_density=0
    )
    
    assert np.isnan(ContaminantVolP), f'Contaminant volume percent calculation failed'


def test_contaminant_volume_percent_from_mixed_density_invalid_density():
    '''
    Test calculation of contaminant volume percent from mixed density when densities are equal.
    Should return nan.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=800,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=800
    )
    
    assert np.isnan(ContaminantVolP), f'Contaminant volume percent calculation failed'


def test_contaminant_volume_percent_from_mixed_density_measured_density_greater():
    '''
    Test calculation of contaminant volume percent from mixed density when measured density is greater than dominant phase density.
    Should return 100.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=1050,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert ContaminantVolP == 100, f'Contaminant volume percent calculation failed'


def test_contaminant_volume_percent_from_mixed_density_measured_density_lower():
    '''
    Test calculation of contaminant volume percent from mixed density when measured density is lower than contaminant phase density.
    Should return 0.
    '''
    
    ContaminantVolP = fluid_mechanics.contaminant_volume_percent_from_mixed_density(
        measured_total_density=750,
        DominantPhase_EOS_density=800,
        ContaminantPhase_EOS_density=1000
    )
    
    assert ContaminantVolP == 0, f'Contaminant volume percent calculation failed'

def test_lockhart_martinelli_parameter_typical():
    """
    Test Lockhart-Martinelli parameter with typical values.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=100,
        mass_flow_rate_gas=50,
        density_liquid=900,
        density_gas=100
    )
    expected = (100 / 50) * ((100 / 900) ** 0.5)
    assert np.isclose(X, expected), f"Lockhart-Martinelli parameter calculation failed: {X} != {expected}"

def test_lockhart_martinelli_parameter_equal_mass_flow_and_density():
    """
    Test Lockhart-Martinelli parameter when mass flow rates and densities are equal.
    Should return 1.0.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=10,
        density_liquid=1000,
        density_gas=1000
    )
    assert X == 1.0, f"Lockhart-Martinelli parameter should be 1.0, got {X}"

def test_lockhart_martinelli_parameter_zero_gas_flow():
    """
    Test Lockhart-Martinelli parameter when gas mass flow rate is zero.
    Should return nan.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=0,
        density_liquid=1000,
        density_gas=100
    )
    assert np.isnan(X), "Lockhart-Martinelli parameter should be nan for zero gas flow"

def test_lockhart_martinelli_parameter_zero_gas_density():
    """
    Test Lockhart-Martinelli parameter when gas density is zero.
    Should return nan.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=5,
        density_liquid=1000,
        density_gas=0
    )
    assert np.isnan(X), "Lockhart-Martinelli parameter should be nan for zero gas density"

def test_lockhart_martinelli_parameter_zero_liquid_density():
    """
    Test Lockhart-Martinelli parameter when liquid density is zero.
    Should return nan.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=5,
        density_liquid=0,
        density_gas=100
    )
    assert np.isnan(X), "Lockhart-Martinelli parameter should be nan for zero liquid density"

def test_lockhart_martinelli_parameter_negative_values():
    """
    Test Lockhart-Martinelli parameter with negative values for mass flow or density.
    Should return nan.
    """
    X1 = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=-5,
        density_liquid=1000,
        density_gas=100
    )
    X2 = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=5,
        density_liquid=-1000,
        density_gas=100
    )
    X3 = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=10,
        mass_flow_rate_gas=5,
        density_liquid=1000,
        density_gas=-100
    )
    assert np.isnan(X1), "Lockhart-Martinelli parameter should be nan for negative gas flow"
    assert np.isnan(X2), "Lockhart-Martinelli parameter should be nan for negative liquid density"
    assert np.isnan(X3), "Lockhart-Martinelli parameter should be nan for negative gas density"

def test_lockhart_martinelli_parameter_liquid_flow_zero():
    """
    Test Lockhart-Martinelli parameter when liquid mass flow rate is zero.
    Should return zero.
    """
    X = fluid_mechanics.lockhart_martinelli_parameter(
        mass_flow_rate_liquid=0,
        mass_flow_rate_gas=10,
        density_liquid=1000,
        density_gas=100
    )
    assert X == 0.0, f"Lockhart-Martinelli parameter should be 0.0 when liquid flow is zero, got {X}"
