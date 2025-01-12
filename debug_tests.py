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

from tests.test_metering import *
from tests.test_thermodynamics import *

if __name__ == '__main__':
    test_calculate_flow_venturi()
    test_calculate_beta_DP_meter()
    test_calculate_expansibility_ventiruri()
    test_calculate_beta_V_cone()
    test_calculate_expansibility_Stewart_V_cone()
    test_V_cone_calculation_1()
    test_V_cone_calculation_2()
    test_natural_gas_viscosity_Lee_et_al()
    test_calculate_expansibility_orifice()
    test_calculate_C_orifice_ReaderHarrisGallagher()
    test_calculate_flow_orifice()
    test_calculate_flow_orifice_without_C()
    test_calculate_flow_orifice_vs_ISO5167_1_E1()
    test_calculate_flow_orifice_invalid_inputs()
    
    print('All tests passed')