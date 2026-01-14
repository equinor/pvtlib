"""MIT License

Copyright (c) 2026 Christian Hågenvik

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

from pvtlib.metering import gas_density_meters

def test_GDM_uncorr_dens():
    
    Du = gas_density_meters.GDM_uncorr_dens(
        tau=657.2723, 
        K0=-109.934, 
        K1=-0.0035718, 
        K2=0.000432733
        )
    
    Dref = 74.662
    
    assert Dref == round(Du,3), 'Error in GDM Du'


def test_GDM_tempcorr_dens():
    '''
    Temperature correction on gas density meter
    The test is based on separate calculation in excel, because no test data was available. The test therefore assumes that the given equation is correct.
    '''
    
    Du = 50.0
    
    Dt = gas_density_meters.GDM_tempcorr_dens(
        Du=Du, 
        K18=-1.7973e-05, 
        K19=3.4502e-04, 
        T=100, 
        Tcal = 20.0
        )
    
    assert Dt == 49.9557096, 'GDM temperature correction failed'

    
def test_Gas_Spesific_Gravity():
    
    SG = gas_density_meters.gas_spesific_gravity(
        MW_gas=20.0, 
        MW_air=28.9647
        )
    
    assert round(SG,4) == 0.6905, 'Error in GDM spesific gravity'


def test_GDM_SOScorr_dens():
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=108.07, 
        tau=714.07, 
        c_cal=372.89, 
        c_gas=418.8, 
        K=2.1e4
        )

    assert round(Dvos,5) == 108.20862, 'GDM speed of sound density failed'


def test_GDM_SOScorr_lowdens_example_from_manual():
    '''
    Example calculation in 7812 Gas Density Meter Installation and Maintenance Manual appendix D.4.1
    VOS correction factor at 10 kg/m3
    '''
    
    rho = 10.0
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=rho, 
        tau=532, 
        c_cal=350, 
        c_gas=441, 
        K=2.1e4
        )
    
    VOS_factor = Dvos / rho
    
    assert (VOS_factor-1.0046)<0.0001, 'GDM speed of sound low density example from 7812 manual failed'

def test_GDM_SOScorr_highdens_example_from_manual():
    '''
    Example calculation in 7812 Gas Density Meter Installation and Maintenance Manual appendix D.4.1
    VOS correction factor at 60 kg/m3

    '''
    
    rho = 60.0
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=rho, 
        tau=633, 
        c_cal=359, 
        c_gas=433, 
        K=2.1e4
        )
    
    VOS_factor = Dvos / rho
    
    assert (VOS_factor-1.0026)<0.0001, 'GDM speed of sound high density example from 7812 manual failed'

def test_GDM_Q():

    Q = gas_density_meters.GDM_Q(
        dP=200.0,
        rho=15.0, 
        K=0.6
        )
    
    assert round(Q,5) == 2.19089, 'Error in GDM Q'


# Tests for invalid input handling (divide by zero protection)

def test_gas_spesific_gravity_zero_MW_air():
    '''Test that gas_spesific_gravity returns NaN when MW_air is zero'''
    import numpy as np
    
    SG = gas_density_meters.gas_spesific_gravity(
        MW_gas=20.0, 
        MW_air=0.0
        )
    
    assert np.isnan(SG), 'gas_spesific_gravity should return NaN when MW_air is zero'


def test_GDM_G_zero_Cp_Cv():
    '''Test that GDM_G returns NaN when Cp_Cv is zero'''
    import numpy as np
    
    G = gas_density_meters.GDM_G(
        SG=0.7, 
        Cp_Cv=0.0
        )
    
    assert np.isnan(G), 'GDM_G should return NaN when Cp_Cv is zero'


def test_GDM_VOScorr_dens_zero_DT_plus_K4():
    '''Test that GDM_VOScorr_dens returns NaN when (DT + K4) is zero'''
    import numpy as np
    
    DV = gas_density_meters.GDM_VOScorr_dens(
        DT=10.0, 
        K3=100.0, 
        K4=-10.0,  # This makes DT + K4 = 0
        G=0.5, 
        t=20.0
        )
    
    assert np.isnan(DV), 'GDM_VOScorr_dens should return NaN when (DT + K4) is zero'


def test_GDM_VOScorr_dens_zero_t_plus_273():
    '''Test that GDM_VOScorr_dens returns NaN when (t + 273) is zero'''
    import numpy as np
    
    DV = gas_density_meters.GDM_VOScorr_dens(
        DT=50.0, 
        K3=100.0, 
        K4=10.0, 
        G=0.5, 
        t=-273.0  # Absolute zero in Celsius
        )
    
    assert np.isnan(DV), 'GDM_VOScorr_dens should return NaN when (t + 273) is zero'


def test_GDM_SOScorr_dens_zero_tau():
    '''Test that GDM_SOScorr_dens returns NaN when tau is zero'''
    import numpy as np
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=50.0, 
        tau=0.0,  # Zero time period
        c_cal=350.0, 
        c_gas=400.0, 
        K=2.1e4
        )
    
    assert np.isnan(Dvos), 'GDM_SOScorr_dens should return NaN when tau is zero'


def test_GDM_SOScorr_dens_zero_c_cal():
    '''Test that GDM_SOScorr_dens returns NaN when c_cal is zero'''
    import numpy as np
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=50.0, 
        tau=600.0, 
        c_cal=0.0,  # Zero speed of sound for calibration gas
        c_gas=400.0, 
        K=2.1e4
        )
    
    assert np.isnan(Dvos), 'GDM_SOScorr_dens should return NaN when c_cal is zero'


def test_GDM_SOScorr_dens_zero_c_gas():
    '''Test that GDM_SOScorr_dens returns NaN when c_gas is zero'''
    import numpy as np
    
    Dvos = gas_density_meters.GDM_SOScorr_dens(
        rho=50.0, 
        tau=600.0, 
        c_cal=350.0, 
        c_gas=0.0,  # Zero speed of sound for process gas
        K=2.1e4
        )
    
    assert np.isnan(Dvos), 'GDM_SOScorr_dens should return NaN when c_gas is zero'


def test_GDM_Q_zero_rho():
    '''Test that GDM_Q returns NaN when rho is zero'''
    import numpy as np
    
    Q = gas_density_meters.GDM_Q(
        dP=200.0, 
        rho=0.0,  # Zero density
        K=0.6
        )
    
    assert np.isnan(Q), 'GDM_Q should return NaN when rho is zero'


def test_GDM_Q_negative_dP():
    '''Test that GDM_Q handles negative differential pressure (reverse flow)'''
    
    Q = gas_density_meters.GDM_Q(
        dP=-200.0,  # Negative dP
        rho=15.0, 
        K=0.6
        )
    
    # Should return negative flow
    assert round(Q,5) == -2.19089, 'GDM_Q should handle negative dP for reverse flow'


def test_GDM_Q_zero_dP():
    '''Test that GDM_Q returns zero when dP is zero'''
    
    Q = gas_density_meters.GDM_Q(
        dP=0.0,  # Zero differential pressure
        rho=15.0, 
        K=0.6
        )
    
    assert Q == 0.0, 'GDM_Q should return zero when dP is zero'