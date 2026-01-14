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

import sys
import os

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