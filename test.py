from pvtlib import AGA8

#Run AGA8 setup for gerg an detail
gerg = AGA8('GERG-2008')

tests = {'case1': {'composition': {'N2': 10.0, 'C1': 90.0}, 'pressure': 20.0, 'enthalpy': -107.60343095444294}}

for case_name, case_dict in tests.items():
    results = gerg.calculate_from_PH(
        composition=case_dict['composition'],
        pressure=case_dict['pressure'],
        enthalpy=case_dict['enthalpy'],
        pressure_unit='bara'
    )

    print(results['temperature_C'])


res2 = gerg.calculate_from_PS(composition={'N2': 10.0, 'C1': 90.0}, pressure=20.0, entropy=-22.2091149233982, pressure_unit='bara')

print(res2['temperature_C'])