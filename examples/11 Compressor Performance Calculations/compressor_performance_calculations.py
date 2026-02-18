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

import pvtlib
import numpy as np

# Gas composition
composition = {
    'N2': 1.0,
    'CO2': 1.0,
    'C1': 90.0,
    'C2': 5.0,
    'C3': 2.0,
    'iC4': 0.5,
    'nC4': 0.5
}

# Compressor operating conditions
P_suction = 60.0  # Suction pressure [bara]
T_suction = 40.0  # Suction temperature [C]
P_discharge = 75.0  # Discharge pressure [bara]
T_discharge = 60.0  # Discharge temperature [C]

# Compressor design parameters
N = 3600  # Compressor speed [rpm]
D = 0.4  # First impeller diameter [m]
Q_inlet = 2.5  # Volumetric flow rate at inlet [m^3/s]
num_impellers = 1  # Number of impellers

print("="*100)
print("COMPRESSOR PERFORMANCE CALCULATIONS".center(100))
print("="*100)

# Set up AGA8 object for GERG-2008 equation
gerg = pvtlib.AGA8('GERG-2008')

# Calculate gas properties at suction conditions
gas_suction = gerg.calculate_from_PT(
    composition=composition,
    pressure=P_suction,
    temperature=T_suction,
)

# Calculate gas properties at discharge conditions
gas_discharge = gerg.calculate_from_PT(
    composition=composition,
    pressure=P_discharge,
    temperature=T_discharge,
)

print("\nGAS PROPERTIES")
print("-"*100)
print(f"{'Property':<40} {'Suction':>25} {'Discharge':>25}")
print("-"*100)
print(f"{'Pressure [bara]':<40} {P_suction:>25.3f} {P_discharge:>25.3f}")
print(f"{'Temperature [°C]':<40} {T_suction:>25.3f} {T_discharge:>25.3f}")
print(f"{'Mass density [kg/m³]':<40} {gas_suction['rho']:>25.3f} {gas_discharge['rho']:>25.3f}")
print(f"{'Molar mass [g/mol]':<40} {gas_suction['mm']:>25.3f} {gas_discharge['mm']:>25.3f}")
print(f"{'Compressibility factor [-]':<40} {gas_suction['z']:>25.6f} {gas_discharge['z']:>25.6f}")
print(f"{'Enthalpy [J/mol]':<40} {gas_suction['h']:>25.3f} {gas_discharge['h']:>25.3f}")

# Convert molar enthalpy to mass enthalpy [kJ/kg]
h_suction_mass = gas_suction['h'] / gas_suction['mm']  # J/mol / g/mol = J/g = kJ/kg
h_discharge_mass = gas_discharge['h'] / gas_discharge['mm']  # J/mol / g/mol = J/g = kJ/kg

print(f"{'Mass enthalpy [kJ/kg]':<40} {h_suction_mass:>25.3f} {h_discharge_mass:>25.3f}")

print("\n" + "="*100)
print("COMPRESSOR PERFORMANCE CALCULATIONS")
print("="*100)

# Calculate polytropic exponent
n = pvtlib.equipment.compressors.poly_exp(
    p_suction=P_suction,
    p_discharge=P_discharge,
    rho_suction=gas_suction['rho'],
    rho_discharge=gas_discharge['rho']
)

print(f"\nPolytropic exponent, n: {n:.6f} [-]")

# Calculate polytropic head
head = pvtlib.equipment.compressors.poly_head(
    n=n,
    p_suction=P_suction,
    p_discharge=P_discharge,
    rho_suction=gas_suction['rho'],
    rho_discharge=gas_discharge['rho']
)

print(f"Polytropic head: {head:.3f} kJ/kg")

# Calculate enthalpy rise
enthalpy_rise = pvtlib.equipment.compressors.dh(
    mass_enthalpy_1=h_suction_mass,
    mass_enthalpy_2=h_discharge_mass
)

print(f"Enthalpy rise, Δh: {enthalpy_rise:.3f} kJ/kg")

# Calculate polytropic efficiency
efficiency = pvtlib.equipment.compressors.poly_eff(
    head=head,
    enthalpy_rise=enthalpy_rise
)

print(f"Polytropic efficiency: {efficiency:.6f} [-] ({efficiency*100:.3f} %)")

# Calculate impeller tangential velocity (tip speed)
tip_speed = pvtlib.equipment.compressors.impeller_tang_vel(
    N=N,
    D=D
)

print(f"\nImpeller tangential velocity (tip speed): {tip_speed:.3f} m/s")

# Calculate sigma U squared (for multiple impellers, create array)
tip_speed_array = np.array([tip_speed] * num_impellers)
sigma_u_sq = pvtlib.equipment.compressors.sigma_u_squared(
    tipSpeedArray=tip_speed_array
)

print(f"Sigma U²: {sigma_u_sq:.1f} J/kg (m²/s²)")

# Calculate polytropic head coefficient
head_coeff = pvtlib.equipment.compressors.poly_head_coeff(
    head=head,
    sigma_u_sq=sigma_u_sq
)

print(f"Polytropic head coefficient, μ: {head_coeff:.6f} [-]")

# Calculate work coefficient
work_coeff = pvtlib.equipment.compressors.work_coefficient(
    enthalpy_rise=enthalpy_rise,
    sigma_u_sq=sigma_u_sq
)

print(f"Work coefficient, λ: {work_coeff:.6f} [-]")

# Calculate flow coefficient (both definitions)
flow_coeff_MAN = pvtlib.equipment.compressors.flow_coeff(
    Q=Q_inlet,
    N=N,
    D=D,
    DefType='MAN'
)

flow_coeff_ISO = pvtlib.equipment.compressors.flow_coeff(
    Q=Q_inlet,
    N=N,
    D=D,
    DefType='ISO 5389'
)

print(f"\nFlow coefficient (MAN definition): {flow_coeff_MAN:.6f} [-]")
print(f"Flow coefficient (ISO 5389 definition): {flow_coeff_ISO:.6f} [-]")

# Calculate mass flow rate and power
mass_flow = Q_inlet * gas_suction['rho']  # kg/s
power = mass_flow * enthalpy_rise  # kW

print(f"\nMass flow rate: {mass_flow:.3f} kg/s")
print(f"Compressor power: {power:.3f} kW")

print("\n" + "="*100)
