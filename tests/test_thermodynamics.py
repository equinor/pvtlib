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

from pvtlib import thermodynamics, unit_converters

def test_natural_gas_viscosity_Lee_et_al():

    # Test data against example data on https://petrowiki.spe.org/Gas_viscosity (Table 1 / name: "table 5.8-values for example problem 6")

    cases={
        'case1':{'P':10.0,'T':20.0,'M':28.01,'rho':12.69,'mu_expected':0.0180},
        # 'case2':{'P':10.0,'T':100.0,'M':18.0,'rho':40.0,'mu_expected':0.0138},
        # 'case3':{'P':10.0,'T':100.0,'M':18.0,'rho':80.0,'mu_expected':0.0138},
    }

    for case_name, case_dict in cases.items():
        mu=thermodynamics.natural_gas_viscosity_Lee_et_al(
            P=case_dict['P'],
            T=case_dict['T'],
            M=case_dict['M'],
            rho=case_dict['rho']
        )
        
        assert mu==pytest.approx(case_dict['mu_expected'],abs=1e-3)

    mu=thermodynamics.natural_gas_viscosity_Lee_et_al(
        

