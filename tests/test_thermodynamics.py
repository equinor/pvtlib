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

from pvtlib import thermodynamics, utilities

def test_natural_gas_viscosity_Lee_et_al():

    # Test data against experimental data from Lee, A.L., M.H. Gonzalez, and B.E. Eakin, The Viscosity of Natural Gases. Journal of Petroleum Technology, 1966 

    cases={
        'case1':{'P':206.84,'T':171.11,'M':18.26,'rho':102.67,'mu_expected':0.01990}, # 3000 psi and 340 F
        'case2':{'P':551.58,'T':37.78,'M':18.26,'rho':309.13,'mu_expected':0.04074}, # 8000 psi and 100 F
        'case3':{'P':27.58,'T':137.78,'M':18.26,'rho':102.67,'mu_expected':0.01602}, # 400 psi and 280 F
    }

    criteria = 1.0 # [%] Acceptable relative error

    for case_name, case_dict in cases.items():
        mu=thermodynamics.natural_gas_viscosity_Lee_et_al(
            P=case_dict['P'],
            T=case_dict['T'],
            M=case_dict['M'],
            rho=case_dict['rho']
        )

        # Calculate relative error
        relative_error=abs(utilities.calculate_relative_deviation(mu,case_dict['mu_expected']))
        
        assert relative_error<criteria, f'Error in {case_name} is {relative_error}'
        


        

