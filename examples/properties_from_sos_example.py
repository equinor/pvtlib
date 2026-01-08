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

# Specify pressure, temperature and composition
P = 50.0  # Pressure [bara]
T = 40.0  # Temperature [C]

composition = {
    'N2': 1.0,
    'CO2': 1.0,
    'C1': 90.0,
    'C2': 5.0,
    'C3': 2.0,
    'iC4': 0.5,
    'nC4': 0.5
}

# First, calculate the "true" properties using AGA8 directly to get a reference speed of sound
gerg = pvtlib.AGA8('GERG-2008')
reference_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Get the reference speed of sound and other properties
measured_sos = reference_properties['w']  # Speed of sound [m/s]
reference_rho = reference_properties['rho']  # Density [kg/m3]
reference_M = reference_properties['mm']  # Molar mass [g/mol = kg/kmol]
reference_Z = reference_properties['Z']  # Compressibility factor [-]

print("Reference properties from GERG-2008:")
print(f"  Speed of sound: {measured_sos:.3f} m/s")
print(f"  Density: {reference_rho:.3f} kg/m3")
print(f"  Molar mass: {reference_M:.3f} kg/kmol")
print(f"  Compressibility factor: {reference_Z:.5f}")
print()

# Now use the properties_from_sos_kappa method to calculate properties from the measured speed of sound
calculated_properties = pvtlib.thermodynamics.properties_from_sos_kappa(
    gas_composition=composition,
    measured_sos=measured_sos,
    pressure_bara=P,
    temperature_C=T,
    EOS='GERG-2008'
)

print("Properties calculated from measured speed of sound:")
print(f"  Density: {calculated_properties['rho']:.3f} kg/m3")
print(f"  Molar mass: {calculated_properties['M']:.3f} kg/kmol")
print(f"  Compressibility factor: {calculated_properties['Z']:.5f}")
print()

# Calculate differences
rho_diff = abs(calculated_properties['rho'] - reference_rho)
M_diff = abs(calculated_properties['M'] - reference_M)
Z_diff = abs(calculated_properties['Z'] - reference_Z)

print("Differences (should be very small due to numerical precision):")
print(f"  Density difference: {rho_diff:.6f} kg/m3")
print(f"  Molar mass difference: {M_diff:.6f} kg/kmol")
print(f"  Compressibility factor difference: {Z_diff:.8f}")
