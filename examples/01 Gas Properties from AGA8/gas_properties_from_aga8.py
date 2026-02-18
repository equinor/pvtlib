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
P = 50.0 # Pressure [bara]
T = 40.0 # Temperature [C]

composition = {
    'N2' : 1.0,
    'CO2' : 1.0,
    'C1' : 90.0,
    'C2' : 5.0,
    'C3' : 2.0,
    'iC4' : 0.5,
    'nC4' : 0.5
}

# Set up AGA8 object for GERG-2008 equation. This process runs the setup for the given equation, and is only needed once.
gerg = pvtlib.AGA8('GERG-2008')

# Calculate gas properties (default pressure and temperature units are bara and C)
gas_properties = gerg.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Set up AGA8 object for DETAIL equation.
detail = pvtlib.AGA8('DETAIL')

# Calculate gas properties
gas_properties_detail = detail.calculate_from_PT(
    composition=composition,
    pressure=P,
    temperature=T,
)

# Print all properties in a table format
print("\n" + "="*100)
print(f"{'Property':<40} {'GERG-2008':>25} {'DETAIL':>25}")
print("="*100)

# Define properties to print with descriptions and units
properties = [
    ('pressure_bara', 'Pressure [bara]'),
    ('temperature_C', 'Temperature [°C]'),
    ('z', 'Compressibility factor [-]'),
    ('rho', 'Mass density [kg/m³]'),
    ('d', 'Molar density [mol/l]'),
    ('mm', 'Molar mass [g/mol]'),
    ('w', 'Speed of sound [m/s]'),
    ('h', 'Enthalpy [J/mol]'),
    ('s', 'Entropy [J/(mol·K)]'),
    ('u', 'Internal energy [J/mol]'),
    ('g', 'Gibbs energy [J/mol]'),
    ('cp', 'Isobaric heat capacity [J/(mol·K)]'),
    ('cv', 'Isochoric heat capacity [J/(mol·K)]'),
    ('kappa', 'Isentropic exponent [-]'),
    ('jt', 'Joule-Thomson coefficient [K/kPa]'),
]

for prop_key, prop_desc in properties:
    gerg_value = gas_properties.get(prop_key, 'N/A')
    detail_value = gas_properties_detail.get(prop_key, 'N/A')
    
    if isinstance(gerg_value, (int, float)) and isinstance(detail_value, (int, float)):
        print(f"{prop_desc:<40} {gerg_value:>25.6f} {detail_value:>25.6f}")
    else:
        print(f"{prop_desc:<40} {str(gerg_value):>25} {str(detail_value):>25}")

print("="*100)