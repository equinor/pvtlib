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
import numpy as np

def GDM_uncorr_dens(tau, K0, K1, K2):
    '''
    Uncorrected density is calculated from instrument time period, described in Eq 2-1 in Micro Motion GDM user manual [1]_.
    
    Parameters
    ----------
    tau : float
        Instrument time period [μs]
    K0 : float
        GDM calibration factor
    K1 : float
        GDM calibration factor
    K2 : float
        GDM calibration factor

    Returns
    -------
    Du : float
        Measured density from GDM, uncorrected [kg/m3]

    References
    ----------
    .. [1] Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual. April 2016
    '''
    Du = K0 + (K1*tau) + (K2*(tau**2))
    
    return Du


def GDM_tempcorr_dens(Du, K18, K19, T, Tcal = 20):
    '''
    Density correction for the difference between the operating temperature and the calibration temperature
    Eq 2-2 in Micro Motion GDM user manual [1]_.
    
    Parameters
    ----------
    Du : float
        Measured density from GDM, uncorrected [kg/m3]
    K18 : float
        GDM calibration factor
    K19 : float
        GDM calibration factor
    T : float
        Measured temperature at GDM [C]
    T_cal : float
        GDM calibration temperature [C]

    Returns
    -------
    DT : float
        Measured density from GDM, corrected for temperature [kg/m3]

    References
    ----------
    .. [1] Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual. April 2016
    '''
    DT = Du*(1 + K18*(T - Tcal)) + K19*(T - Tcal)
    
    return DT


def gas_spesific_gravity(MW_gas, MW_air = 28.96469):
    '''
    Calculate gas spesific gravity as described in eq 2-4 Micro Motion GDM user manual [1]_.
    
    Parameters
    ----------
    MW_gas : float
        Gas molecular weight [kg/kmol]
    MW_air : float, optional
        Air molecular weight [kg/kmol]. The default is 28.96469.

    Returns
    -------
    Gas spesific gravity [-]

    References
    ----------
    .. [1] Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual. April 2016
    '''
    
    return MW_gas/MW_air

  
def GDM_G(SG , Cp_Cv ):
    '''
    Calculate G, the ratio between spesific gravity and Cp/Cv, used in the GDM VOS correction.
    Cp/Cv should be calculated at base conditions: 1.01325 barA and 20 C, according to Micro Motion.
    
    Parameters
    ----------
    SG : float
        Gas spesific gravity [-]
    Cp_Cv : float
        Cp/Cv [-]

    Returns
    -------
    G : float
        Ratio between SG and Cp/Cv

    References
    ----------
    .. [1] Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual. April 2016
    '''

    return SG / Cp_Cv


def GDM_VOScorr_dens(DT, K3, K4, G, t , A = 0.00236):
    '''
    Speed of sound density correction, as given in calibration certificates. Corresponds to eq 2-3 in Micro Motion GDM user manual [1]_.
    The correction is performed to take into account the difference in properties between the calibration gas and the actual process gas
    
    This method is referred to as the "User Gas Equation Method" in the MicroMotion 7812 manual [2]_, and is a simplified approach.
    
    Parameters
    ----------
    DT : float
        Measured density from GDM, corrected for temperature [kg/m3]
    K3 : float
        GDM calibration factor
    K4 : float
        GDM calibration factor
    G : float
        Gas spesific gravity / Ratio of spesific heats
    t : float
        Measured temperature at GDM [C]

    Returns
    -------
    Dvos : float
        Measured density from GDM, corrected for speed of sound [kg/m3]

    References
    ----------
    .. [1] Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual. April 2016
    .. [2] Micro Motion® Installation and Maintenance Manual - 7812 Gas Density Meter. 2012
    '''
    
    DV = DT*(1 + ((K3/(DT + K4))*(A - (G/(t + 273)))))
    
    return DV


def GDM_SOScorr_dens(rho, tau, c_cal, c_gas, K=2.1e4):
    '''
    Speed of sound density correction. The correction is performed to take into account the difference in properties between the calibration gas and the actual process gas.
    The correction factor is given by equation E7 in the Installation and Maintenance Manual for Micro Motion 7812 (P/N MMI-20018377, Rev. AC April 2012) [1_]. 
    The equation originates from "Velocity of Sound Effect on Gas Density Transducers - The theory, measurement results and methods of correction", by Stansfeld, J W (NSFMW 1986) [2_].

    Parameters
    ----------
    rho : float
        Measured density from GDM, corrected for temperature [kg/m3].
    tau : float
        Measured instrument time period [μs].
    c_cal : float
        Speed of sound of calibration gas [m/s]
        The conditions of this values are not specified in the manual, however, after checking with both Micro Motion and Kiwa, and they both say that they believe the following:
        The speed of sound of the calibration gas should be at the same density (or time period) as during calibration (according to Micro Motion: email from Rik Gerritsen 2023-12-18)
    c_gas : float
        Speed of sound of measured gas [m/s] at measured conditions (also confirmed by vendor).
    K : float, optional
        Speed of sound constant for density sensor. The default is 2.1e4 for both the Micro Motion 7812 and the GDM (also confirmed by vendor)

    Returns
    -------
    rho_vos : float
        Measured density from GDM, corrected for speed of sound [kg/m3]

    References
    ----------
    .. [1] Micro Motion® Installation and Maintenance Manual - 7812 Gas Density Meter. 2012
    .. [2] Stansfeld, J W (NSFMW 1986) "Velocity of Sound Effect on Gas Density Transducers - The theory, measurement results and methods of correction"
    '''
    
    if tau==0 or c_cal==0 or c_gas==0:
        return np.nan
    
    rho_vos = rho*((1+((K/(tau*c_cal))**2))/(1+((K/(tau*c_gas))**2)))
                   
    return rho_vos
    

def GDM_Q(dP, rho, K):
    '''
    Equation used to calculate the volume flowrate through a device, for example two GDMs. 
    According to GDM manual, the flowrate through the GDM should be around 5 l/h, and within 1-10 l/h. 
    A version of the equation is given in the Micro Motion 7812 manual chapter 3.6 [1]_, with K=0.5. 
    
    Parameters
    ----------
    dP : float
        Measured differential pressure accross device. For example dP accross two GDMs [mbar]
    rho : float
        Measured gas density [kg/m3]
    K : float
        K-factor. Determined from flow calibration []

    Returns
    -------
    Q : float
        Volume flowrate through device [l/h]

    References
    ----------
    .. [1] Micro Motion® Installation and Maintenance Manual - 7812 Gas Density Meter. 2012
    '''
    
    #velger å tillate negativ flow slik vi kan bruke dette ifm feilsøking
    if dP >= 0:
        Q = K * math.sqrt( dP / rho )
    else:
        Q = -K * math.sqrt( -dP / rho )

    return Q


def gas_density_from_SOS_and_IE(SOS, IE, P_bara):
    '''
    Calculate gas density from speed of sound, isentropic exponent and pressure.
    The method is described in [1]_ from the GFMW2024. 

    Parameters
    ----------
    SOS : float
        Gas Speed of Sound [m/s]
    IE : float
        Isentropic Exponent [-]
    P_bara : float
        Pressure [bara]

    Returns
    -------
    rho : float
        Gas density [kg/m3]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    
    P_Pa = P_bara*10**5
    
    if SOS==0:
        rho = np.nan
    else:
        rho = IE * P_Pa/(SOS**2)
    
    return rho


def gas_SOS_from_density_and_IE(rho, IE, P_bara):
    '''
    Calculate gas speed of sound from density, isentropic exponent and pressure
    The method is described in [1]_ from the GFMW2024.

    Parameters
    ----------
    rho : float
        Gas density [kg/m3]

    IE : float
        Isentropic Exponent [-]
    P_bara : float
        Pressure [bara]

    Returns
    -------
    SOS : float
        Gas Speed of Sound [m/s]

    References
    ----------
    .. [1] Hågenvik, C., D. Van Putten, and D. Mæland, Exploring the Relationship between Speed of Sound, Density, and Isentropic Exponent. Global Flow Measurement Workshop, 2024
    '''
    
    P_Pa = P_bara*10**5
    
    if rho==0:
        SOS = np.nan
    else:
        SOS = np.sqrt(IE * P_Pa/rho)
    
    return SOS