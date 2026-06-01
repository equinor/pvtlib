from pvtlib.metering import coriolis_flowmeters


def test_coriolis_pressure_corrections_micromotion_reference_data():
    """Validate pressure corrections using Micro Motion ELITE PDS reference points."""
    p_act = 25.0  # bara
    p_cal = 1.0   # bara

    cases = [
        ("CMF025H", 500.0, 800.0, 0.0, -0.058, 500.0, 798.608),
        ("CMF050H", 2000.0, 800.0, 0.0, 0.029, 2000.0, 800.696),
        ("CMF100H", 10000.0, 800.0, 0.003, 0.087, 10007.2, 802.088),
        ("CMF300H", 80000.0, 800.0, 0.006, -0.0029, 80115.2, 799.9304),
        ("CMF400H", 200000.0, 800.0, 0.012, 0.145, 200576.0, 803.48),
    ]

    for _, m_meas, rho_meas, p_cm, p_cd, m_expected, rho_expected in cases:
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
