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