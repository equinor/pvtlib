from pvtlib.metering import coriolis_flowmeters


def test_coriolis_pressure_corrections_from_micromotion_process_pressure_effects():
    """Validate equations using Micro Motion ELITE PDS process-pressure effects.

    Note: This test validates the equation/sign convention with PDS pressure-effect
    coefficients. It does not claim that corrected mass flow and density values are
    tabulated reference output points in the PDS.

    The equations are valid for Emerson Micro Motion Coriolis flowmeters and can
    be used for other Coriolis meters if PCm/PCd are defined exactly as in the
    equation docstrings (opposite sign of datasheet process-pressure effect).
    """
    p_act = 25.0  # bara
    p_cal = 1.0   # bara

    cases = [
        # model, m_meas[kg/h], rho_meas[kg/m3],
        # PDS mass effect[%/bar], PDS density effect[kg/m3/bar],
        # expected m_corr[kg/h], expected rho_corr[kg/m3]
        ("CMF025H", 500.0, 800.0, 0.0, 0.058, 500.0, 798.608),
        ("CMF050H", 2000.0, 800.0, 0.0, -0.029, 2000.0, 800.696),
        ("CMF100H", 10000.0, 800.0, -0.003, -0.087, 10007.2, 802.088),
        ("CMF300H", 80000.0, 800.0, -0.006, 0.0029, 80115.2, 799.9304),
        ("CMF400H", 200000.0, 800.0, -0.012, -0.145, 200576.0, 803.48),
    ]

    for _, m_meas, rho_meas, pds_mass_effect, pds_density_effect, m_expected, rho_expected in cases:
        # Equation inputs PCm/PCd are opposite sign of PDS process-pressure effect.
        p_cm = -pds_mass_effect
        p_cd = -pds_density_effect
        m_corr = coriolis_flowmeters.coriolis_massflow_corr_pres(
            m_meas=m_meas, P_act=p_act, PCm=p_cm, P_cal=p_cal
        )
        rho_corr = coriolis_flowmeters.coriolis_dens_corr_pres(
            rho_meas=rho_meas, P_act=p_act, PCd=p_cd, P_cal=p_cal
        )

        assert abs(m_corr - m_expected) < 1e-9
        assert abs(rho_corr - rho_expected) < 1e-9


def test_coriolis_massflow_cut_off():
    assert coriolis_flowmeters.coriolis_massflow_cut_off(12.5, 10.0) == 12.5
    assert coriolis_flowmeters.coriolis_massflow_cut_off(10.0, 10.0) == 0.0
