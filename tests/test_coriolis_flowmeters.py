from pvtlib.metering import coriolis_flowmeters


def test_coriolis_pressure_corrections_from_micromotion_process_pressure_effects():
    """Validate equations using Micro Motion ELITE PDS process-pressure effects.

    The equations are applicable to the Emerson Micro Motion Coriolis flowmeters. 
    The test cases are derived from the process-pressure effect values provided in the Micro Motion ELITE PDS (PS-00374, Rev AO, December 2024).
    The correction factors (PCm for mass flow and PCd for density) are provided
    directly in each test case.
    """
    p_act = 25.0  # bara
    p_cal = 1.0   # bara

    cases = [
        {
            "model": "CMF025H",
            "inputs": {"m_meas": 500.0, "rho_meas": 800.0},
            "correction_factors": {"PCm": 0.0, "PCd": -0.058},
            "expected": {"m_corr": 500.0, "rho_corr": 798.608},
        },
        {
            "model": "CMF050H",
            "inputs": {"m_meas": 2000.0, "rho_meas": 800.0},
            "correction_factors": {"PCm": 0.0, "PCd": 0.029},
            "expected": {"m_corr": 2000.0, "rho_corr": 800.696},
        },
        {
            "model": "CMF100H",
            "inputs": {"m_meas": 10000.0, "rho_meas": 800.0},
            "correction_factors": {"PCm": 0.003, "PCd": 0.087},
            "expected": {"m_corr": 10007.2, "rho_corr": 802.088},
        },
        {
            "model": "CMF300H",
            "inputs": {"m_meas": 80000.0, "rho_meas": 800.0},
            "correction_factors": {"PCm": 0.006, "PCd": -0.0029},
            "expected": {"m_corr": 80115.2, "rho_corr": 799.9304},
        },
        {
            "model": "CMF400H",
            "inputs": {"m_meas": 200000.0, "rho_meas": 800.0},
            "correction_factors": {"PCm": 0.012, "PCd": 0.145},
            "expected": {"m_corr": 200576.0, "rho_corr": 803.48},
        },
    ]

    for case in cases:
        m_corr = coriolis_flowmeters.coriolis_massflow_corr_pres(
            m_meas=case["inputs"]["m_meas"],
            P_act=p_act,
            PCm=case["correction_factors"]["PCm"],
            P_cal=p_cal,
        )
        rho_corr = coriolis_flowmeters.coriolis_dens_corr_pres(
            rho_meas=case["inputs"]["rho_meas"],
            P_act=p_act,
            PCd=case["correction_factors"]["PCd"],
            P_cal=p_cal,
        )

        assert abs(m_corr - case["expected"]["m_corr"]) < 1e-9
        assert abs(rho_corr - case["expected"]["rho_corr"]) < 1e-9


def test_coriolis_massflow_cut_off():
    assert coriolis_flowmeters.coriolis_massflow_cut_off(12.5, 10.0) == 12.5
    assert coriolis_flowmeters.coriolis_massflow_cut_off(10.0, 10.0) == 0.0
