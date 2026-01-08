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
P = 100.0  # Pressure [bara]
T = 50.0  # Temperature [C]
measured_sos = 433.0  # Speed of sound [m/s]

composition = {
    'N2': 1.0,
    'CO2': 2.0,
    'C1': 90.0,
    'C2': 6.4,
    'C3': 0.5,
    'iC4': 0.05,
    'nC4': 0.05
}

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



# Alternatively, the properties can be calculated by individual functions

# Step 1: Calculate properties using composition, P, and T. 

gerg = pvtlib.AGA8('GERG-2008')

# Calculate properties using composition, P, and T and the GERG-2008 EOS
gerg_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Step 2: Calculate properties from measured speed of sound

molar_mass_from_sos = pvtlib.thermodynamics.molar_mass_from_sos_kappa(
    measured_sos=measured_sos,
    kappa= gerg_properties['kappa'],
    Z=gerg_properties['z'],
    temperature_C=T
)

density_from_sos_kappa = pvtlib.thermodynamics.density_from_sos_kappa(
    measured_sos=measured_sos,
    kappa=gerg_properties['kappa'],
    Z=gerg_properties['z'],
    temperature_C=T
)

Z_from_sos_kappa = pvtlib.thermodynamics.Z_from_sos_kappa(
    measured_sos=measured_sos,
    kappa=gerg_properties['kappa'],
    Z=gerg_properties['z'],
    temperature_C=T
)

print("Properties calculated from measured speed of sound (using kappa, Z, T):")
print(f"  Molar mass from SOS: {molar_mass_from_sos:.3f} kg/kmol")
print(f"  Density from SOS: {density_from_sos_kappa:.3f} kg/m3")
print(f"  Compressibility factor from SOS: {Z_from_sos_kappa:.5f}")