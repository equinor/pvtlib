import math
import numpy as np

def Kv(Q, SG, dP):
    '''
    Kv is the flow factor (expressed in m3/h), and is the metric equivalent of Cv (flow coefficient of a device).
    
    Kv is proportional to the Cv.         
    
    .. math::
        Kv = Q\sqrt{\frac{SG}{dP}}
        
        {\displaystyle C_{\text{v}}=1.156\cdot K_{\text{v}}.}

    https://en.wikipedia.org/wiki/Flow_coefficient

    Parameters
    ----------
    Q : TYPE
        Q is the flowrate [m3/h].
    SG : TYPE
        SG is the specific gravity of the fluid (for water = 1).
    dP : TYPE
        dP is the differential pressure across the device [bar].

    Returns
    -------
    Kv : float
        The flow factor (expressed in m3/h)

    '''
    
    if dP!=0 and (SG/dP)>=0:
        Kv = Q*math.sqrt(SG/dP)
    else:
        Kv = np.nan
        
    return Kv


def Q_from_Kv(Kv, SG, dP):
    '''
    Parameters
    ----------
    Kv : TYPE
        The flow factor (expressed in m3/h)
    SG : TYPE
        SG is the specific gravity of the fluid (for water = 1).
    dP : TYPE
        dP is the differential pressure across the device [bar].

    Returns
    -------
    Q : float
        Q is the flowrate [m3/h].

    '''
    
    if dP>0 and SG>0 and math.sqrt(SG/dP)!=0:
        Q = Kv/math.sqrt(SG/dP)
    else:
        Q = np.nan
        
    return Q