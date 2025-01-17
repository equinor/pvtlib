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
    