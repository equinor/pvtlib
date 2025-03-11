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

from pvtlib import AGA8

# Fluid: 90% methane and 10% nitrogen at 20 C
# What is the temperature after an isenthalpic expansion from 100 bara to 80 bara?

# Define the gas composition
composition = {'C1': 0.9, 'N2': 0.1}

# Define the initial conditions
P1 = 100  # bara
T1 = 20  # C

# Define the final conditions
P2 = 80  # bara

# Run AGA8 setup for GERG-2008
gerg = AGA8('GERG-2008')

# Calculate the enthalpy at the initial conditions
res1 = gerg.calculate_from_PT(pressure=P1, temperature=T1, composition=composition)

# Calculate the temperature at the final conditions
res2 = gerg.calculate_from_PH(pressure=P2, enthalpy=res1['h'], composition=composition)

# Print the results
print(f'The temperature after the expansion is {res2["temperature_C"]:.2f} C\n')

# Print gas density and speed of sound after the expansion
print(f'Gas properties after the expansion:')
print(f'The gas density is {res2["rho"]:.2f} kg/m3')
print(f'The speed of sound is {res2["w"]:.2f} m/s\n')

# What is the temperature after an isentropic process from 100 bara to 80 bara?

# Calculate the temperature at the final conditions
res3 = gerg.calculate_from_PS(pressure=P2, entropy=res1['s'], composition=composition)

# Print the results
print(f'The temperature after the isentropic process is {res3["temperature_C"]:.2f} C\n')
