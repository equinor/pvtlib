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


def coriolis_dens_corr_pres(rho_meas, P_act, PCd, P_cal):
    """Correct Coriolis measured density for pressure effect.

    These equations are validated for Emerson Micro Motion Coriolis flowmeters
    using process-pressure-effect values from the ELITE process data sheet (PDS).
    They can also be used for other Coriolis meters if the factors are aligned
    with the definitions below.

    Parameters
    ----------
    rho_meas : float
        Measured density from Coriolis meter [kg/m3].
    P_act : float
        Actual process pressure [bara].
    PCd : float
        Density correction factor [kg/m3/bar]. This must be the opposite sign of
        the process-pressure effect published in the meter process data sheet.
    P_cal : float
        Meter calibration pressure [bara].

    Returns
    -------
    float
        Density corrected for pressure effect [kg/m3].
    """
    return rho_meas + PCd * (P_act - P_cal)


def coriolis_massflow_corr_pres(m_meas, P_act, PCm, P_cal):
    """Correct Coriolis measured mass flow for pressure effect.

    These equations are validated for Emerson Micro Motion Coriolis flowmeters
    using process-pressure-effect values from the ELITE process data sheet (PDS).
    They can also be used for other Coriolis meters if the factors are aligned
    with the definitions below.

    Parameters
    ----------
    m_meas : float
        Measured mass flow from Coriolis meter [kg/h].
    P_act : float
        Actual process pressure [bara].
    PCm : float
        Mass-flow correction factor [%/bar]. This must be the opposite sign of
        the process-pressure effect published in the meter process data sheet.
    P_cal : float
        Meter calibration pressure [bara].

    Returns
    -------
    float
        Mass flow corrected for pressure effect [kg/h].
    """
    return m_meas * (1 + (PCm / 100) * (P_act - P_cal))


def coriolis_massflow_cut_off(m_meas, cut_off):
    """Apply a mass-flow cut-off to measured Coriolis flow [kg/h]."""
    if m_meas > cut_off:
        return m_meas
    return 0.0
