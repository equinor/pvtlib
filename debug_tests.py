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

import tests.test_differential_pressure_flowmeters as dp_tests
import tests.test_thermodynamics as thermo_tests

if __name__ == '__main__':
    dp_tests.test_calculate_flow_venturi()
    dp_tests.test_calculate_beta_DP_meter()
    dp_tests.test_calculate_expansibility_ventiruri()
    dp_tests.test_calculate_beta_V_cone()
    dp_tests.test_calculate_expansibility_Stewart_V_cone()
    dp_tests.test_V_cone_calculation_1()
    dp_tests.test_V_cone_calculation_2()
    thermo_tests.test_natural_gas_viscosity_Lee_et_al()
    dp_tests.test_calculate_expansibility_orifice()
    dp_tests.test_calculate_C_orifice_ReaderHarrisGallagher()
    dp_tests.test_calculate_flow_orifice()
    dp_tests.test_calculate_flow_orifice_without_C()
    dp_tests.test_calculate_flow_orifice_vs_ISO5167_1_E1()
    dp_tests.test_calculate_flow_orifice_invalid_inputs()
    
    print('All tests passed')