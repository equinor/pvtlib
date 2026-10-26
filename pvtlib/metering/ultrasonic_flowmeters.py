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

from pvtlib import fluid_mechanics as _fm


#%% Wet-gas over-reading correction of van Putten et al., NSFMW 2015
# Simplified gas-void-fraction model, Equations (29)-(30). Over-reading is
# modelled as Q_indicated / Q_actual = 1 / alpha_gas, Equation (12).
# The critical gas Froude number comes from WLR, Equation (27), or from the
# gas Ohnesorge number, Equation (26). These are alternative simplifications;
# neither implements the full physical model of Equation (28).
# Liquid loading, fluid properties and any dry-gas baseline correction must be
# established independently; nothing is calibrated or inferred here.
# https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf

def gas_void_fraction_low_froude_VanPutten_2015(X):
    """
    Calculate the gas void fraction below the critical gas Froude number.

    Uses the first expression for chi(X) in Equation (30), not the
    alternative fitted approximation. This is the low-Froude branch of
    Equation (29).

    Parameters
    ----------
    X : float
        Non-negative Lockhart-Martinelli liquid-loading parameter [-].

    Returns
    -------
    alpha : float
        Fraction of the pipe volume occupied by gas [-], not the flowing
        gas volume fraction (GVF). Dry gas (X = 0) gives 1.
        NaN for non-finite/negative X or a predicted fraction outside (0, 1].

    Notes
    -----
    ``chi = 1 / (1 + X) - X**0.76 + 1.44 * X``.
    The JIP range extends to X = 0.30. Values above this are extrapolation,
    even when the returned fraction is physically bounded.

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equations (29)-(30).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    if not np.isfinite(X) or X < 0:
        return np.nan

    # Add the empirical hold-up adjustment to the stratified-flow expression.
    alpha = 1 / (1 + X) - X**0.76 + 1.44 * X
    return alpha if np.isfinite(alpha) and 0 < alpha <= 1 else np.nan


def critical_froude_from_WLR_VanPutten_2015(WLR=0.0):
    """
    Estimate the stratified-to-dispersed transition Froude number from WLR.

    Implements the simplified interpolation ``Fr_crit = 1.2 + 0.3 * WLR``.

    Parameters
    ----------
    WLR : float, optional
        Water volume flow / total liquid volume flow [-], in [0, 1].
        Default 0 represents hydrocarbon liquid; 1 represents water.

    Returns
    -------
    Fr_gas_crit : float
        Critical gas densimetric Froude number [-].
        NaN for non-finite WLR or values outside [0, 1].

    See Also
    --------
    critical_froude_from_Ohnesorge_VanPutten_2015 : Fluid-property alternative.

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equation (27).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    if not np.isfinite(WLR) or not 0 <= WLR <= 1:
        return np.nan

    return 1.2 + 0.3 * WLR


def critical_froude_from_Ohnesorge_VanPutten_2015(rho_g, mu_g, surface_tension, D):
    """
    Estimate the transition Froude number from gas properties and diameter.

    Implements ``Fr_crit = 2.3e-5 * Oh_gas**(-1.1)``. This alternative to
    the WLR approximation requires independently supplied fluid properties.

    Parameters
    ----------
    rho_g : float
        Positive gas density at line conditions [kg/m3].
    mu_g : float
        Positive gas dynamic viscosity at line conditions [Pa.s].
    surface_tension : float
        Positive gas-liquid interfacial tension at line conditions [N/m].
    D : float
        Positive inner pipe diameter [m].

    Returns
    -------
    Fr_gas_crit : float
        Critical gas densimetric Froude number [-].
        NaN for non-finite or non-physical input/result.

    Notes
    -----
    Gas properties, not liquid viscosity, define Oh_gas in this correlation.
    For an oil-water mixture, Equation (43) provides a simplified linear rule
    weighted by the liquid volumetric-flow split, implemented in
    ``fluid_mechanics.gas_liquid_interfacial_tension_linear_mixing``.
    Choosing this transition correlation does not implement Equation (28).

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equations (25)-(26).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    # Combine gas viscosity, density and interfacial tension into Oh_gas.
    Oh_gas = _fm.ohnesorge_number(mu_g, rho_g, D, surface_tension)
    if not np.isfinite(Oh_gas) or Oh_gas <= 0:
        return np.nan

    Fr_gas_crit = 2.3e-5 * Oh_gas**(-1.1)
    return Fr_gas_crit if np.isfinite(Fr_gas_crit) and Fr_gas_crit > 0 else np.nan


def gas_void_fraction_VanPutten_2015(X, Fr_gas, GVF, Fr_gas_crit=1.2):
    """
    Calculate gas void fraction across the low- and high-Froude branches.

    Below the transition, use the low-Froude correlation. Above it,
    relax exponentially towards the no-slip limit GVF.

    Parameters
    ----------
    X : float
        Non-negative Lockhart-Martinelli parameter [-].
    Fr_gas : float
        Non-negative gas densimetric Froude number based on actual gas
        flow, not the over-reading indicated flow [-].
    GVF : float
        Flowing gas volume fraction at line conditions [-], in (0, 1].
        Must describe the same liquid loading and densities as X.
    Fr_gas_crit : float, optional
        Positive transition Froude number [-]. Default 1.2 is the
        WLR = 0 value. Either critical-Froude helper can supply this input.

    Returns
    -------
    alpha_gas : float
        Gas void fraction and indicated-flow correction multiplier [-].
        Model over-reading is ``1 / alpha_gas``.
        NaN for non-finite/non-physical input or a non-physical prediction.

    Notes
    -----
    Above the transition, ``alpha = (chi - GVF) *
    exp(-0.4 * (Fr_gas - Fr_gas_crit)) + GVF``.
    Both branches meet continuously at Fr_gas_crit. Without densities this
    function cannot check consistency between X and GVF; the flow wrapper
    computes both from a common set of inputs.

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Equations (29)-(30).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    if (not np.all(np.isfinite([X, Fr_gas, GVF, Fr_gas_crit]))
            or X < 0 or Fr_gas < 0 or not 0 < GVF <= 1 or Fr_gas_crit <= 0):
        return np.nan

    alpha_low = gas_void_fraction_low_froude_VanPutten_2015(X)
    if not np.isfinite(alpha_low):
        return np.nan

    if Fr_gas < Fr_gas_crit:
        # Below the transition, the simplified hold-up depends only on X.
        return alpha_low

    # At higher Froude number, relax towards the no-slip flow fraction.
    return (alpha_low - GVF) * np.exp(-0.4 * (Fr_gas - Fr_gas_crit)) + GVF


def check_operating_point_DNV_USM_wetgas_JIP_2015(GVF, X, DR, Fr_gas):
    """
    Check an operating point against the DNV USM wet-gas JIP ranges reported in 2015.

    Parameters
    ----------
    GVF : float
        Flowing gas volume fraction at line conditions [-].
    X : float
        Lockhart-Martinelli parameter [-].
    DR : float
        Gas-to-liquid density ratio [-].
    Fr_gas : float
        Gas densimetric Froude number at corrected gas flow [-].

    Returns
    -------
    checks : dict
        Boolean entries ``GVF``, ``X``, ``DR`` and ``Fr_gas``. True means
        the individual value is within the checked range:
        0.95 < GVF <= 1, 0 <= X <= 0.30, 0.010 <= DR <= 0.032,
        and 0.7 <= Fr_gas <= 2.2. Non-finite input gives False.

    Notes
    -----
    Checks only GVF, Lockhart-Martinelli parameter, density ratio and gas
    densimetric Froude number against the ranges reported in the 2015 NSFMW
    paper [1]. The year identifies that publication, not the test dates.
    This is an operating-range check, not a wet-gas correction calculation.
    Does not assess consistency between inputs, diameter, orientation,
    pressure, temperature, fluid properties or meter suitability.
    The JIP used a horizontal 6-inch line at 12-32 bara and 15-35 degC,
    with natural gas, Exxsol D120 and saline water.
    Passing all checks does not establish model accuracy for a meter.
    An out-of-range flag denotes extrapolation, not necessarily an
    unphysical input. The X = 0 limit includes the analytical dry-gas case.

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015, Sections 3 and 5.2.1.
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    return {
        "GVF": bool(np.isfinite(GVF) and 0.95 < GVF <= 1),
        "X": bool(np.isfinite(X) and 0 <= X <= 0.30),
        "DR": bool(np.isfinite(DR) and 0.010 <= DR <= 0.032),
        "Fr_gas": bool(np.isfinite(Fr_gas) and 0.7 <= Fr_gas <= 2.2),
    }


def calculate_flow_wetgas_USM_VanPutten_2015(
    VolFlow_gas_measured, D, rho_g, rho_l, GVF=None, GMF=None,
    WLR=0.0, Fr_gas_crit=None, check_input=False,
):
    """
    Apply the Van Putten (2015) wet-gas over-reading correction to a USM.

    Corrects an ultrasonic meter's indicated gas volume flow for the
    over-reading predicted under wet-gas conditions. Solves
    ``Q_actual = alpha_gas(Q_actual) * Q_indicated`` using the simplified
    Van Putten model from the 2015 NSFMW paper. Liquid loading must be supplied
    independently; the meter reading alone cannot determine it.

    Parameters
    ----------
    VolFlow_gas_measured : float
        Non-negative indicated gas flow at line conditions [m3/h].
        Any established dry-gas calibration must already have been applied.
        This function applies only the wet-gas over-reading correction.
    D : float
        Positive inner pipe diameter [m].
    rho_g : float
        Positive gas density at line conditions [kg/m3].
    rho_l : float
        Liquid density at the same conditions, greater than rho_g [kg/m3].
        For oil/water, a supplied volume-weighted mixture density may be
        calculated using ``fluid_mechanics.mixture_density_homogeneous``.
        It must be consistent with WLR; no properties are inferred here.
    GVF : float, optional
        Flowing gas volume fraction [-], in (0, 1]. Supply GVF or GMF.
        If both are supplied, GVF takes precedence and GMF is recalculated.
        Both supplied fractions must nevertheless be valid.
    GMF : float, optional
        Gas mass fraction [-], in (0, 1]. Converted to GVF when GVF is absent.
    WLR : float, optional
        Water volume flow / total liquid volume flow [-], in [0, 1].
        Default 0. Used only for the default critical-Froude correlation.
        Ignored, including validation, when Fr_gas_crit is supplied.
    Fr_gas_crit : float, optional
        Positive critical gas Froude number [-]. If omitted, calculated
        from WLR, Equation (27). To use Equation (26), supply the result of
        ``critical_froude_from_Ohnesorge_VanPutten_2015`` explicitly.
    check_input : bool, optional
        If True, raise on invalid input or calculation failure. If False
        (default), return NaN numerical fields and a descriptive ``error``.
        Incorrect argument types can raise regardless of this setting.

    Returns
    -------
    results : dict
        Fields (all flow rates are at line conditions):

        - ``VolFlow_gas_measured``: supplied indicated gas flow [m3/h].
        - ``VolFlow_gas_corrected``: corrected gas flow [m3/h].
        - ``VolFlow_liq``: liquid flow inferred from the supplied fraction [m3/h].
        - ``VolFlow_tot``: corrected gas plus liquid flow [m3/h].
        - ``MassFlow_gas``, ``MassFlow_liq``: phase mass flows [kg/h].
        - ``OverRead``: indicated/actual flow factor, 1/alpha_gas [-].
        - ``alpha_gas``: gas void fraction / applied correction multiplier [-].
        - ``LockhartMartinelli``: liquid-loading parameter X [-].
        - ``Fr_gas``: gas Froude number at the returned corrected flow [-].
        - ``Fr_gas_crit``: transition Froude number used [-].
        - ``GVF``, ``GMF``: consistent gas flow fractions [-].
        - ``DR``: rho_g/rho_l [-].
        - ``iterations``: number of fixed-point iterations.
        - ``within_JIP_envelope``: whether all four dimensionless checks pass.
        - ``JIP_envelope_exceeded``: tuple of failed check names.
        - ``error``: None on success, otherwise a failure description.

        On failure all numerical fields are NaN, the envelope flag is False
        and the exceeded tuple is empty because no range assessment was made.

    Raises
    ------
    ValueError
        If input values are invalid and check_input is True.
    RuntimeError
        If a non-physical result or non-convergence occurs and check_input
        is True.

    Notes
    -----
    The corrected flow determines superficial gas velocity and Fr_gas,
    which in turn determines alpha_gas. Fixed-point iteration starts with
    the indicated flow and stops at a relative flow change below 1e-10,
    with at most 100 iterations. At zero indicated flow all phase flows
    are zero; OverRead is the model factor, not an observed 0/0 ratio.

    Uses Equations (29)-(30), not the full physical model of Equation (28).
    The four JIP checks are diagnostics only; extrapolation is not blocked
    unless the prediction is non-physical. Passing them does not establish
    meter suitability or validate an uncertainty claim.

    Examples
    --------
    Illustrative inputs only, not measured data or a calibration:

    >>> result = calculate_flow_wetgas_USM_VanPutten_2015(
    ...     VolFlow_gas_measured=1000, D=0.15, rho_g=20, rho_l=1000,
    ...     GVF=0.99, WLR=0.5, check_input=True,
    ... )
    >>> result["error"] is None
    True

    References
    ----------
    .. [1] van Putten et al., "Ultrasonic Meters in Wet Gas Application",
       North Sea Flow Measurement Workshop (NSFMW), 2015,
       Equations (4), (7), (12), (26)-(30) and (40).
       https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf
    """
    results = dict.fromkeys((
        "VolFlow_gas_measured", "VolFlow_gas_corrected", "VolFlow_liq",
        "VolFlow_tot", "MassFlow_gas", "MassFlow_liq", "OverRead",
        "alpha_gas", "LockhartMartinelli", "Fr_gas", "Fr_gas_crit",
        "GVF", "GMF", "DR", "iterations",
    ), np.nan)
    results.update(within_JIP_envelope=False, JIP_envelope_exceeded=(), error=None)

    # Reject missing/non-physical inputs before calculating ratios or roots.
    error = None
    if not np.all(np.isfinite([VolFlow_gas_measured, D, rho_g, rho_l])):
        error = "Flow, diameter and densities must be finite."
    elif VolFlow_gas_measured < 0 or D <= 0 or rho_g <= 0 or rho_l <= rho_g:
        error = "Require flow >= 0, D > 0 and rho_l > rho_g > 0."
    elif GVF is None and GMF is None:
        error = "Either GVF or GMF must be supplied."
    elif GVF is not None and (not np.isfinite(GVF) or not 0 < GVF <= 1):
        error = "GVF must be finite and in (0, 1]."
    elif GMF is not None and (not np.isfinite(GMF) or not 0 < GMF <= 1):
        error = "GMF must be finite and in (0, 1]."
    elif Fr_gas_crit is None and (not np.isfinite(WLR) or not 0 <= WLR <= 1):
        error = "WLR must be finite and in [0, 1] when no critical Froude is supplied."
    elif Fr_gas_crit is not None and (not np.isfinite(Fr_gas_crit) or Fr_gas_crit <= 0):
        error = "Critical Froude number must be finite and positive."

    if error is not None:
        if check_input:
            raise ValueError(error)
        results["error"] = error
        return results

    # Establish consistent flow fractions and liquid loading at line conditions.
    if GVF is None:
        GVF = _fm.GMF_to_GVF(GMF, rho_g, rho_l)
    GMF = _fm.GVF_to_GMF(GVF, rho_g, rho_l)
    X = _fm.GVF_to_lockhart_martinelli(GVF, rho_l, rho_g)
    DR = _fm.gas_liquid_density_ratio(rho_g, rho_l)

    # Use the WLR approximation unless the caller explicitly selected another Fr*.
    if Fr_gas_crit is None:
        Fr_gas_crit = critical_froude_from_WLR_VanPutten_2015(WLR)

    # Fr_gas requires the unknown actual flow; start with the indicated rate.
    corrected_flow = VolFlow_gas_measured
    for iteration in range(1, 101):
        velocity = _fm.superficial_velocity(corrected_flow, D)
        Fr_gas = _fm.densimetric_froude_number(velocity, D, rho_g, rho_l)
        alpha_gas = gas_void_fraction_VanPutten_2015(X, Fr_gas, GVF, Fr_gas_crit)

        if not np.isfinite(alpha_gas):
            error = "Van Putten model produced a non-physical gas void fraction."
            break

        # Equation (12): the occupied liquid volume reduces actual gas flow.
        next_flow = alpha_gas * VolFlow_gas_measured
        converged = next_flow == 0 or abs(next_flow - corrected_flow) < 1e-10 * next_flow
        corrected_flow = next_flow
        if converged:
            break
    else:
        error = "Van Putten wet-gas correction did not converge in 100 iterations."

    if error is not None:
        if check_input:
            raise RuntimeError(error)
        results["error"] = error
        return results

    # Report Froude at the returned flow, not the preceding iteration's estimate.
    velocity = _fm.superficial_velocity(corrected_flow, D)
    Fr_gas = _fm.densimetric_froude_number(velocity, D, rho_g, rho_l)
    liquid_flow = corrected_flow * (1 - GVF) / GVF

    # Derive the phase rates and expose the model quantities for engineering review.
    results.update({
        "VolFlow_gas_measured": VolFlow_gas_measured,
        "VolFlow_gas_corrected": corrected_flow,
        "VolFlow_liq": liquid_flow,
        "VolFlow_tot": corrected_flow + liquid_flow,
        "MassFlow_gas": corrected_flow * rho_g,
        "MassFlow_liq": liquid_flow * rho_l,
        "OverRead": 1 / alpha_gas,
        "alpha_gas": alpha_gas,
        "LockhartMartinelli": X,
        "Fr_gas": Fr_gas,
        "Fr_gas_crit": Fr_gas_crit,
        "GVF": GVF,
        "GMF": GMF,
        "DR": DR,
        "iterations": iteration,
    })
    numerical = [value for key, value in results.items()
                 if key not in ("within_JIP_envelope", "JIP_envelope_exceeded", "error")]
    if not np.all(np.isfinite(numerical)):
        error = "Van Putten calculation produced non-finite flow results."
        if check_input:
            raise RuntimeError(error)
        results.update({key: np.nan for key in results
                        if key not in ("within_JIP_envelope", "JIP_envelope_exceeded", "error")})
        results["error"] = error
        return results

    # Check only the documented dimensionless ranges, not overall meter suitability.
    checks = check_operating_point_DNV_USM_wetgas_JIP_2015(GVF, X, DR, Fr_gas)
    results["within_JIP_envelope"] = all(checks.values())
    results["JIP_envelope_exceeded"] = tuple(name for name, inside in checks.items() if not inside)
    return results