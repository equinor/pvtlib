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
        # case1, case2 and case3 are from the paper (sample 4) where mu_expected is the experimental value of viscosity (mu_E). Use a accept criteria of 10% for these
        # however, I was not able to reproduce the calculated values (mu_c) from the paper. Could be an error in the paper..?
        'case1':{'T':171.11,'M':18.26,'rho':105.6,'mu_expected':0.01990 , 'criteria':10.0}, # 3000 psi and 340 F
        'case2':{'T':37.78,'M':18.26,'rho':310.6,'mu_expected':0.04074, 'criteria':10.0}, # 8000 psi and 100 F 309.13 g/cc
        'case3':{'T':137.78,'M':18.26,'rho':15.1,'mu_expected':0.01602, 'criteria':10.0}, # 400 psi and 280 F
        
        # case4 is from calculation example at https://petrowiki.spe.org/Gas_viscosity. This is reproduced identically. 
        'case4':{'T':65.55,'M':20.079,'rho':110.25,'mu_expected':0.01625, 'criteria':0.1}, # 60 F, 0.7 g/cc
    }


    for case_name, case_dict in cases.items():
        mu=thermodynamics.natural_gas_viscosity_Lee_et_al(
            T=case_dict['T'],
            M=case_dict['M'],
            rho=case_dict['rho']
        )

        # Calculate relative error
        relative_error=abs(utilities.calculate_relative_deviation(mu,case_dict['mu_expected']))
        
        assert relative_error<case_dict['criteria'], f'Natural gas viscosity calculation failed for {case_name}'
        


        

