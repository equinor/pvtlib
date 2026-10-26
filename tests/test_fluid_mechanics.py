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

def test_dominant_phase_corrected_density_4():
    '''
    Test calculation of dominant phase corrected density.
    Example: Contaminant volume fraction is 0 vol%, should return measured density.
    '''

    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=900,
        ContaminantVolP=0,
        ContaminantPhase_EOS_density=1000
    )

    assert round(corrected_density, 2) == 900.0, f'Dominant phase corrected density calculation failed'

def test_dominant_phase_corrected_density_5():
    '''
    Test calculation of dominant phase corrected density.
    Example: Contaminant volume fraction is 0 vol% and ContaminantPhase_EOS_density is np.nan, should return measured density.
    '''

    corrected_density = fluid_mechanics.dominant_phase_corrected_density(
        measured_total_density=900,
        ContaminantVolP=0,
        ContaminantPhase_EOS_density=np.nan
    )

    assert round(corrected_density, 2) == 900.0, f'Dominant phase corrected density calculation failed'

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


def test_reynolds_number_laminar():
    """
    Test reynolds_number in the laminar regime (Re < 2300).
    rho=1000 kg/m3, v=0.01 m/s, D=0.1 m, mu=0.001 Pa·s → Re = 1000
    """
    Re = fluid_mechanics.reynolds_number(rho=1000, v=0.01, D=0.1, mu=0.001)
    assert np.isclose(Re, 1000.0), f'reynolds_number laminar case failed: {Re} != 1000.0'


def test_reynolds_number_turbulent():
    """
    Test reynolds_number in the turbulent regime (Re > 4000).
    rho=1000 kg/m3, v=1.0 m/s, D=0.1 m, mu=0.001 Pa·s → Re = 100000
    """
    Re = fluid_mechanics.reynolds_number(rho=1000, v=1.0, D=0.1, mu=0.001)
    assert np.isclose(Re, 100000.0), f'reynolds_number turbulent case failed: {Re} != 100000.0'


def test_reynolds_number_invalid_inputs():
    """
    Test reynolds_number returns np.nan for non-positive inputs.
    """
    assert np.isnan(fluid_mechanics.reynolds_number(rho=0, v=1.0, D=0.1, mu=0.001)), 'rho<=0 should return nan'
    assert np.isnan(fluid_mechanics.reynolds_number(rho=1000, v=0, D=0.1, mu=0.001)), 'v<=0 should return nan'
    assert np.isnan(fluid_mechanics.reynolds_number(rho=1000, v=1.0, D=0, mu=0.001)), 'D<=0 should return nan'
    assert np.isnan(fluid_mechanics.reynolds_number(rho=1000, v=1.0, D=0.1, mu=0)), 'mu<=0 should return nan'


def test_superficial_velocity_typical():
    """
    Test superficial_velocity with typical inputs.
    Q_phase=1.0 m3/h, D=0.1 m → Us = (1/3600) / (pi*(0.05)^2)
    """
    from math import pi
    Q, D = 1.0, 0.1
    expected = (Q / 3600) / (pi * (D / 2) ** 2)
    result = fluid_mechanics.superficial_velocity(Q_phase=Q, D=D)
    assert np.isclose(result, expected), f'superficial_velocity typical case failed: {result} != {expected}'


def test_superficial_velocity_zero_diameter():
    """
    Test superficial_velocity returns np.nan when D=0 (pipe area is zero).
    """
    result = fluid_mechanics.superficial_velocity(Q_phase=1.0, D=0)
    assert np.isnan(result), f'superficial_velocity D=0 should return nan, got {result}'


def test_liquid_holdup_from_density_above_liquid():
    """
    Test liquid_holdup_from_density when measured density exceeds liquid density.
    Should return 1.0.
    """
    result = fluid_mechanics.liquid_holdup_from_density(
        measured_density=900, liquid_density=800, gas_density=100
    )
    assert result == 1.0, f'liquid holdup above liquid density should be 1.0, got {result}'


def test_liquid_holdup_from_density_below_gas():
    """
    Test liquid_holdup_from_density when measured density is below gas density.
    Should return 0.0.
    """
    result = fluid_mechanics.liquid_holdup_from_density(
        measured_density=50, liquid_density=800, gas_density=100
    )
    assert result == 0.0, f'liquid holdup below gas density should be 0.0, got {result}'


def test_liquid_holdup_from_density_midpoint():
    """
    Test liquid_holdup_from_density at a midpoint value.
    gas=100, liquid=800, measured=450 → (450-100)/(800-100) = 0.5
    """
    result = fluid_mechanics.liquid_holdup_from_density(
        measured_density=450, liquid_density=800, gas_density=100
    )
    expected = (450 - 100) / (800 - 100)
    assert np.isclose(result, expected), f'liquid holdup midpoint failed: {result} != {expected}'


def test_liquid_holdup_from_density_equal_densities():
    """
    Test liquid_holdup_from_density when liquid_density == gas_density.
    Should return np.nan (undefined).
    """
    result = fluid_mechanics.liquid_holdup_from_density(
        measured_density=500, liquid_density=500, gas_density=500
    )
    assert np.isnan(result), f'liquid holdup equal densities should return nan, got {result}'


#%% Tests of dimensionless numbers and conversions used in wet-gas calculations

def test_froude_number_wetgas():
    """
    Test the Froude number [-] for reference and boundary inputs.

    Inputs are chosen so that the expected value is exact or a simple root, to
    make the arithmetic easy to reproduce by hand. The Froude cases use a
    diameter equal to the standard acceleration of free fall, 9.80665 m/s2,
    so that the two cancel.
    """
    cases = {
        'Froude number': {
            'input': {
                'v': 9.80665,  # Velocity [m/s]
                'D': 9.80665,  # Pipe diameter [m]
            },
            'expected': 1.0},
        'Froude number, wet-gas conditions': {
            'input': {
                'v': 15.0,  # Velocity [m/s]
                'D': 0.15,  # Pipe diameter [m]
            },
            'expected': 12.367596045581745}, 
        'Froude number, zero velocity': {
            'input': {
                'v': 0.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
            },
            'expected': 0.0},
    }

    for name, case in cases.items():
        result = fluid_mechanics.froude_number(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_densimetric_froude_number_wetgas():
    """Test the densimetric Froude number [-] for reference and boundary inputs."""
    cases = {
        'Densimetric Froude number': {
            'input': {
                'v': 9.80665,  # Velocity [m/s]
                'D': 9.80665,  # Pipe diameter [m]
                'rho_phase': 1.0,  # Flowing phase density [kg/m3]
                'rho_other': 2.0,  # Other phase density [kg/m3]
            },
            'expected': 1.0}, 
        'Densimetric Froude number, wet-gas conditions': {
            'input': {
                'v': 15.0,  # Velocity [m/s]
                'D': 0.15,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 915.0,  # Other phase density [kg/m3]
            },
            'expected': 1.8487950594895735}, 
        'Densimetric Froude number, zero velocity': {
            'input': {
                'v': 0.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 1000.0,  # Other phase density [kg/m3]
            },
            'expected': 0.0}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.densimetric_froude_number(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_ohnesorge_number_wetgas():
    """Test the Ohnesorge number [-] for reference inputs."""
    cases = {
        'Ohnesorge number': {
            'input': {
                'mu': 0.02,  # Dynamic viscosity [Pa.s]
                'rho': 4.0,  # Density [kg/m3]
                'D': 0.25,  # Pipe diameter [m]
                'surface_tension': 0.04,  # Surface tension [N/m]
            },
            'expected': 0.1}, 
        'Ohnesorge number, wet-gas conditions': {
            'input': {
                'mu': 1.2e-5,  # Dynamic viscosity [Pa.s]
                'rho': 20.0,  # Density [kg/m3]
                'D': 0.15,  # Pipe diameter [m]
                'surface_tension': 0.04,  # Surface tension [N/m]
            },
            'expected': 3.464101615137755e-05}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.ohnesorge_number(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_gas_liquid_density_ratio_wetgas():
    """Test the gas-to-liquid density ratio [-], including inverted densities."""
    cases = {
        'Density ratio, gas over liquid': {
            'input': {
                'rho_gas': 20.0,  # Gas density [kg/m3]
                'rho_liquid': 1000.0,  # Liquid density [kg/m3]
            },
            'expected': 0.02}, 
        'Density ratio, oil-water mixture': {
            'input': {
                'rho_gas': 20.0,  # Gas density [kg/m3]
                'rho_liquid': 915.0,  # Liquid density [kg/m3]
            },
            'expected': 0.02185792349726776}, 
        'Density ratio, inverted densities': {
            'input': {
                'rho_gas': 1000.0,  # Gas density [kg/m3]
                'rho_liquid': 20.0,  # Liquid density [kg/m3]
            },
            'expected': 50.0}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.gas_liquid_density_ratio(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_GVF_to_lockhart_martinelli_wetgas():
    """Test the Lockhart-Martinelli parameter [-], including dry gas."""
    cases = {
        'Lockhart-Martinelli from GVF': {
            'input': {
                'GVF': 0.8,  # Gas volume fraction [-]
                'density_liquid': 100.0,  # Liquid density [kg/m3]
                'density_gas': 4.0,  # Gas density [kg/m3]
            },
            'expected': 1.25},
        'Lockhart-Martinelli from GVF, wet-gas conditions': {
            'input': {
                'GVF': 0.99,  # Gas volume fraction [-]
                'density_liquid': 915.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': 0.06832196595186203},
        'Lockhart-Martinelli from GVF, dry gas': {
            'input': {
                'GVF': 1.0,  # Gas volume fraction [-]
                'density_liquid': 100.0,  # Liquid density [kg/m3]
                'density_gas': 4.0,  # Gas density [kg/m3]
            },
            'expected': 0.0}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.GVF_to_lockhart_martinelli(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_lockhart_martinelli_to_GVF_wetgas():
    """Test the gas volume fraction [-], including dry gas."""
    cases = {
        'GVF from Lockhart-Martinelli': {
            'input': {
                'X': 1.25,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 100.0,  # Liquid density [kg/m3]
                'density_gas': 4.0,  # Gas density [kg/m3]
            },
            'expected': 0.8}, 
        'GVF from Lockhart-Martinelli, wet-gas conditions': {
            'input': {
                'X': 0.1,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 915.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': 0.9854309693283027}, 
        'GVF from Lockhart-Martinelli, dry gas': {
            'input': {
                'X': 0.0,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 100.0,  # Liquid density [kg/m3]
                'density_gas': 4.0,  # Gas density [kg/m3]
            },
            'expected': 1.0}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.lockhart_martinelli_to_GVF(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_gas_liquid_interfacial_tension_linear_mixing_wetgas():
    """Test gas-liquid interfacial tension [N/m], including pure oil and water."""
    cases = {
        'Liquid mixture surface tension': {
            'input': {
                'WLR': 0.25,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': 0.03}, 
        'Liquid mixture surface tension, pure oil': {
            'input': {
                'WLR': 0.0,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': 0.02},
        'Liquid mixture surface tension, pure water': {
            'input': {
                'WLR': 1.0,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': 0.06},
    }

    for name, case in cases.items():
        result = fluid_mechanics.gas_liquid_interfacial_tension_linear_mixing(**case['input'])
        assert np.isclose(result, case['expected'], rtol=1e-12, atol=1e-14), \
            f'{name}: got {result}, expected {case["expected"]}'


def test_froude_number_wetgas_invalid_inputs():
    """Expect NaN for the Froude number [-] with non-physical inputs."""
    cases = {
        'Froude number, negative velocity': {
            'input': {
                'v': -1.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
            },
            'expected': np.nan}, 
        'Froude number, zero diameter': {
            'input': {
                'v': 1.0,  # Velocity [m/s]
                'D': 0.0,  # Pipe diameter [m]
            },
            'expected': np.nan}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.froude_number(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_densimetric_froude_number_wetgas_invalid_inputs():
    """Expect NaN for the densimetric Froude number [-] with invalid inputs."""
    cases = {
        'Densimetric Froude number, negative velocity': {
            'input': {
                'v': -1.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 1000.0,  # Other phase density [kg/m3]
            },
            'expected': np.nan}, 
        'Densimetric Froude number, zero diameter': {
            'input': {
                'v': 1.0,  # Velocity [m/s]
                'D': 0.0,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 1000.0,  # Other phase density [kg/m3]
            },
            'expected': np.nan}, 
        'Densimetric Froude number, zero phase density': {
            'input': {
                'v': 1.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
                'rho_phase': 0.0,  # Flowing phase density [kg/m3]
                'rho_other': 1000.0,  # Other phase density [kg/m3]
            },
            'expected': np.nan}, 
        'Densimetric Froude number, equal densities': {
            'input': {
                'v': 1.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 20.0,  # Other phase density [kg/m3]
            },
            'expected': np.nan}, 
        'Densimetric Froude number, heavier phase is lighter': {
            'input': {
                'v': 1.0,  # Velocity [m/s]
                'D': 0.1,  # Pipe diameter [m]
                'rho_phase': 20.0,  # Flowing phase density [kg/m3]
                'rho_other': 10.0,  # Other phase density [kg/m3]
            },
            'expected': np.nan}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.densimetric_froude_number(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_ohnesorge_number_wetgas_invalid_inputs():
    """Expect NaN for the Ohnesorge number [-] with non-physical inputs."""
    cases = {
        'Ohnesorge number, zero viscosity': {
            'input': {
                'mu': 0.0,  # Dynamic viscosity [Pa.s]
                'rho': 20.0,  # Density [kg/m3]
                'D': 0.1,  # Pipe diameter [m]
                'surface_tension': 0.04,  # Surface tension [N/m]
            },
            'expected': np.nan}, 
        'Ohnesorge number, zero density': {
            'input': {
                'mu': 1e-5,  # Dynamic viscosity [Pa.s]
                'rho': 0.0,  # Density [kg/m3]
                'D': 0.1,  # Pipe diameter [m]
                'surface_tension': 0.04,  # Surface tension [N/m]
            },
            'expected': np.nan}, 
        'Ohnesorge number, zero diameter': {
            'input': {
                'mu': 1e-5,  # Dynamic viscosity [Pa.s]
                'rho': 20.0,  # Density [kg/m3]
                'D': 0.0,  # Pipe diameter [m]
                'surface_tension': 0.04,  # Surface tension [N/m]
            },
            'expected': np.nan}, 
        'Ohnesorge number, zero surface tension': {
            'input': {
                'mu': 1e-5,  # Dynamic viscosity [Pa.s]
                'rho': 20.0,  # Density [kg/m3]
                'D': 0.1,  # Pipe diameter [m]
                'surface_tension': 0.0,  # Surface tension [N/m]
            },
            'expected': np.nan}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.ohnesorge_number(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_gas_liquid_density_ratio_wetgas_invalid_inputs():
    """Expect NaN for the gas-to-liquid density ratio [-] with zero densities."""
    cases = {
        'Density ratio, zero gas density': {
            'input': {
                'rho_gas': 0.0,  # Gas density [kg/m3]
                'rho_liquid': 1000.0,  # Liquid density [kg/m3]
            },
            'expected': np.nan}, 
        'Density ratio, zero liquid density': {
            'input': {
                'rho_gas': 20.0,  # Gas density [kg/m3]
                'rho_liquid': 0.0,  # Liquid density [kg/m3]
            },
            'expected': np.nan}, 
    }

    for name, case in cases.items():
        result = fluid_mechanics.gas_liquid_density_ratio(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_GVF_to_lockhart_martinelli_wetgas_invalid_inputs():
    """Expect NaN for the Lockhart-Martinelli parameter [-] with invalid inputs."""
    cases = {
        'Lockhart-Martinelli from GVF, zero GVF': {
            'input': {
                'GVF': 0.0,  # Gas volume fraction [-]
                'density_liquid': 1000.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
        'Lockhart-Martinelli from GVF, GVF above one': {
            'input': {
                'GVF': 1.01,  # Gas volume fraction [-]
                'density_liquid': 1000.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
        'Lockhart-Martinelli from GVF, zero liquid density': {
            'input': {
                'GVF': 0.99,  # Gas volume fraction [-]
                'density_liquid': 0.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
        'Lockhart-Martinelli from GVF, zero gas density': {
            'input': {
                'GVF': 0.99,  # Gas volume fraction [-]
                'density_liquid': 1000.0,  # Liquid density [kg/m3]
                'density_gas': 0.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
    }

    for name, case in cases.items():
        result = fluid_mechanics.GVF_to_lockhart_martinelli(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_lockhart_martinelli_to_GVF_wetgas_invalid_inputs():
    """Expect NaN for the gas volume fraction [-] with non-physical inputs."""
    cases = {
        'GVF from Lockhart-Martinelli, negative X': {
            'input': {
                'X': -0.1,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 1000.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
        'GVF from Lockhart-Martinelli, zero liquid density': {
            'input': {
                'X': 0.1,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 0.0,  # Liquid density [kg/m3]
                'density_gas': 20.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
        'GVF from Lockhart-Martinelli, zero gas density': {
            'input': {
                'X': 0.1,  # Lockhart-Martinelli parameter [-]
                'density_liquid': 1000.0,  # Liquid density [kg/m3]
                'density_gas': 0.0,  # Gas density [kg/m3]
            },
            'expected': np.nan},
    }

    for name, case in cases.items():
        result = fluid_mechanics.lockhart_martinelli_to_GVF(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_gas_liquid_interfacial_tension_linear_mixing_wetgas_invalid_inputs():
    """Expect NaN for gas-liquid interfacial tension [N/m] with invalid inputs."""
    cases = {
        'Liquid mixture surface tension, negative WLR': {
            'input': {
                'WLR': -0.1,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': np.nan},
        'Liquid mixture surface tension, WLR above one': {
            'input': {
                'WLR': 1.1,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': np.nan},
        'Liquid mixture surface tension, zero oil surface tension': {
            'input': {
                'WLR': 0.0,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.0,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
            },
            'expected': np.nan},
        'Liquid mixture surface tension, zero water surface tension': {
            'input': {
                'WLR': 1.0,  # Water-to-liquid volume ratio [-]
                'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
                'surface_tension_water': 0.0,  # Gas-water interfacial tension [N/m]
            },
            'expected': np.nan},
    }

    for name, case in cases.items():
        result = fluid_mechanics.gas_liquid_interfacial_tension_linear_mixing(**case['input'])
        assert np.isnan(result), f'{name}: expected nan, got {result}'


def test_froude_number_wetgas_nonfinite_inputs():
    """Expect NaN for the Froude number [-] when any input is NaN or infinite."""
    valid_input = {
        'v': 1.0,  # Velocity [m/s]
        'D': 0.1,  # Pipe diameter [m]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.froude_number(**invalid_input)
            assert np.isnan(result), \
                f'Froude number with {argument}={nonfinite}: expected nan, got {result}'


def test_densimetric_froude_number_wetgas_nonfinite_inputs():
    """Expect NaN for the densimetric Froude number [-] for nonfinite inputs."""
    valid_input = {
        'v': 1.0,  # Velocity [m/s]
        'D': 0.1,  # Pipe diameter [m]
        'rho_phase': 20.0,  # Flowing phase density [kg/m3]
        'rho_other': 1000.0,  # Other phase density [kg/m3]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.densimetric_froude_number(**invalid_input)
            assert np.isnan(result), \
                f'Densimetric Froude number with {argument}={nonfinite}: expected nan, got {result}'


def test_ohnesorge_number_wetgas_nonfinite_inputs():
    """Expect NaN for the Ohnesorge number [-] for nonfinite inputs."""
    valid_input = {
        'mu': 1e-5,  # Dynamic viscosity [Pa.s]
        'rho': 20.0,  # Density [kg/m3]
        'D': 0.1,  # Pipe diameter [m]
        'surface_tension': 0.04,  # Surface tension [N/m]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.ohnesorge_number(**invalid_input)
            assert np.isnan(result), \
                f'Ohnesorge number with {argument}={nonfinite}: expected nan, got {result}'


def test_gas_liquid_density_ratio_wetgas_nonfinite_inputs():
    """Expect NaN for the gas-to-liquid density ratio [-] for nonfinite inputs."""
    valid_input = {
        'rho_gas': 20.0,  # Gas density [kg/m3]
        'rho_liquid': 1000.0,  # Liquid density [kg/m3]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.gas_liquid_density_ratio(**invalid_input)
            assert np.isnan(result), \
                f'Density ratio with {argument}={nonfinite}: expected nan, got {result}'


def test_GVF_to_lockhart_martinelli_wetgas_nonfinite_inputs():
    """Expect NaN for the Lockhart-Martinelli parameter [-] for nonfinite inputs."""
    valid_input = {
        'GVF': 0.99,  # Gas volume fraction [-]
        'density_liquid': 1000.0,  # Liquid density [kg/m3]
        'density_gas': 20.0,  # Gas density [kg/m3]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.GVF_to_lockhart_martinelli(**invalid_input)
            assert np.isnan(result), \
                f'Lockhart-Martinelli from GVF with {argument}={nonfinite}: expected nan, got {result}'


def test_lockhart_martinelli_to_GVF_wetgas_nonfinite_inputs():
    """Expect NaN for the gas volume fraction [-] for nonfinite inputs."""
    valid_input = {
        'X': 0.1,  # Lockhart-Martinelli parameter [-]
        'density_liquid': 1000.0,  # Liquid density [kg/m3]
        'density_gas': 20.0,  # Gas density [kg/m3]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.lockhart_martinelli_to_GVF(**invalid_input)
            assert np.isnan(result), \
                f'GVF from Lockhart-Martinelli with {argument}={nonfinite}: expected nan, got {result}'


def test_gas_liquid_interfacial_tension_linear_mixing_wetgas_nonfinite_inputs():
    """Expect NaN for gas-liquid interfacial tension [N/m] for nonfinite inputs."""
    valid_input = {
        'WLR': 0.5,  # Water-to-liquid volume ratio [-]
        'surface_tension_oil': 0.02,  # Gas-oil interfacial tension [N/m]
        'surface_tension_water': 0.06,  # Gas-water interfacial tension [N/m]
    }

    for argument in valid_input:
        for nonfinite in [np.nan, np.inf, -np.inf]:
            invalid_input = dict(valid_input)
            invalid_input[argument] = nonfinite
            result = fluid_mechanics.gas_liquid_interfacial_tension_linear_mixing(**invalid_input)
            assert np.isnan(result), \
                f'Liquid mixture surface tension with {argument}={nonfinite}: expected nan, got {result}'


def test_lockhart_martinelli_volume_and_mass_forms_are_equivalent():
    """
    Test that the Lockhart-Martinelli parameter calculated from GVF matches the
    mass flow rate form, and that the conversion back to GVF is consistent.

    A total volume flow rate of 100 m3/h is used to obtain the phase mass flow
    rates in kg/h. The total flow rate cancels in the mass flow rate ratio.
    """
    rho_liquid = 800.0  # Liquid density [kg/m3]
    rho_gas = 20.0  # Gas density [kg/m3]
    VolFlow_tot = 100.0  # Total volume flow rate [m3/h]

    for GVF in [
        0.96,  # Gas volume fraction [-]
        0.99,  # Gas volume fraction [-]
        0.999,  # Gas volume fraction [-]
        1.0,  # Gas volume fraction [-]
    ]:
        X = fluid_mechanics.GVF_to_lockhart_martinelli(
            GVF=GVF, density_liquid=rho_liquid, density_gas=rho_gas)

        X_from_mass_flow = fluid_mechanics.lockhart_martinelli_parameter(
            mass_flow_rate_liquid=(1 - GVF) * VolFlow_tot * rho_liquid,
            mass_flow_rate_gas=GVF * VolFlow_tot * rho_gas,
            density_liquid=rho_liquid,
            density_gas=rho_gas)

        GVF_recalculated = fluid_mechanics.lockhart_martinelli_to_GVF(
            X=X, density_liquid=rho_liquid, density_gas=rho_gas)

        assert np.isclose(X, X_from_mass_flow, rtol=1e-12), \
            f'GVF={GVF}: X from GVF {X} does not match X from mass flow rates {X_from_mass_flow}'
        assert np.isclose(GVF_recalculated, GVF, rtol=1e-12), \
            f'GVF={GVF}: GVF recalculated from X gave {GVF_recalculated}'


def test_densimetric_Froude_number_wetgas_cases():
    """
    Test densimetric_froude_number [-] for ten wet-gas cases.

    The gas mass flow rates are in kg/s and are converted to a superficial gas
    velocity before the Froude number is calculated.

    The expected values were calculated outside pvtlib using the decimal module
    at 50 digit precision, with the standard acceleration of free fall
    g_n = 9.80665 m/s2.
    """
    cases = {
        1: { 
            'massflow_gas': 7.5,  # Gas mass flow rate [kg/s]
            'D': 0.2,  # Pipe diameter [m]
            'rho_g': 50,  # Gas density [kg/m3]
            'rho_l': 800.0,  # Liquid density [kg/m3]
            'Frg_expected': 0.8802791617359484,  # Densimetric Froude number [-]
        },
        2: { 
            'massflow_gas': 5.5,  # Gas mass flow rate [kg/s]
            'D': 0.3,  # Pipe diameter [m]
            'rho_g': 50,  # Gas density [kg/m3]
            'rho_l': 800.0,  # Liquid density [kg/m3]
            'Frg_expected': 0.234257605452225,  # Densimetric Froude number [-]
        },
        3: { 
            'massflow_gas': 6.5,  # Gas mass flow rate [kg/s]
            'D': 0.4,  # Pipe diameter [m]
            'rho_g': 50,  # Gas density [kg/m3]
            'rho_l': 1000.0,  # Liquid density [kg/m3]
            'Frg_expected': 0.11983021936627286,  # Densimetric Froude number [-]
        },
        4: { 
            'massflow_gas': 7.0,  # Gas mass flow rate [kg/s]
            'D': 0.1,  # Pipe diameter [m]
            'rho_g': 60,  # Gas density [kg/m3]
            'rho_l': 850.0,  # Liquid density [kg/m3]
            'Frg_expected': 4.133887466692981,  # Densimetric Froude number [-]
        },
        5: { 
            'massflow_gas': 4.5,  # Gas mass flow rate [kg/s]
            'D': 0.1,  # Pipe diameter [m]
            'rho_g': 55,  # Gas density [kg/m3]
            'rho_l': 600.0,  # Liquid density [kg/m3]
            'Frg_expected': 3.341817267513907,  # Densimetric Froude number [-]
        },
        6: { 
            'massflow_gas': 8.0,  # Gas mass flow rate [kg/s]
            'D': 0.15,  # Pipe diameter [m]
            'rho_g': 70,  # Gas density [kg/m3]
            'rho_l': 950.0,  # Liquid density [kg/m3]
            'Frg_expected': 1.5039079811568052,  # Densimetric Froude number [-]
        },
        7: { 
            'massflow_gas': 3.0,  # Gas mass flow rate [kg/s]
            'D': 0.05,  # Pipe diameter [m]
            'rho_g': 40,  # Gas density [kg/m3]
            'rho_l': 800.0,  # Liquid density [kg/m3]
            'Frg_expected': 12.514376965656087,  # Densimetric Froude number [-]
        },
        8: { 
            'massflow_gas': 9.5,  # Gas mass flow rate [kg/s]
            'D': 0.12,  # Pipe diameter [m]
            'rho_g': 65,  # Gas density [kg/m3]
            'rho_l': 1000.0,  # Liquid density [kg/m3]
            'Frg_expected': 3.1409265980080594,  # Densimetric Froude number [-]
        },
        9: { 
            'massflow_gas': 5.5,  # Gas mass flow rate [kg/s]
            'D': 0.1,  # Pipe diameter [m]
            'rho_g': 75,  # Gas density [kg/m3]
            'rho_l': 800.0,  # Liquid density [kg/m3]
            'Frg_expected': 3.0325839725209764,  # Densimetric Froude number [-]
        },
        10: { 
            'massflow_gas': 6.0,  # Gas mass flow rate [kg/s]
            'D': 0.1,  # Pipe diameter [m]
            'rho_g': 45,  # Gas density [kg/m3]
            'rho_l': 700.0,  # Liquid density [kg/m3]
            'Frg_expected': 4.493390102353033,  # Densimetric Froude number [-]
        },
    }

    for i, case in cases.items():
        velocity = fluid_mechanics.superficial_velocity(
            Q_phase=case['massflow_gas'] * 3600 / case['rho_g'],  # Convert to m3/h
            D=case['D']
        )

        Frg = fluid_mechanics.densimetric_froude_number(
            v=velocity,
            D=case['D'],
            rho_phase=case['rho_g'],
            rho_other=case['rho_l']
        )

        assert np.isclose(Frg, case['Frg_expected'], rtol=1e-8), \
            f"Case {i}: Froude number mismatch: got {Frg}, expected {case['Frg_expected']}"
