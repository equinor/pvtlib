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

# Example: Overread correction for wetgas venturi, using the Reader-Harris, Graham correlation.

from pvtlib.metering import differential_pressure_flowmeters
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

venturi = {
    'D': 0.2,          # m, inlet inner diameter
    'd': 0.1,          # m, throat inner diameter
    'P1' : 45.0,       # bara, static pressure at inlet
    'DP' : 600.0,      # mbar, differential pressure
    'rho_g' : 30.0,    # kg/m3, gas density
    'rho_l' : 750.0,   # kg/m3, liquid density
    'H' : 1.0,         # Dimensionless fluid parameter (1 for hydrocarbon liquids, 1.35 for water)
    'kappa' : 1.3,     # isentropic exponent
}

GVF = np.linspace(0.95, 0.999, 100)  # Gas volume fraction from 0.95 to 0.99

results = {}

idx = 0

for gvf in GVF:
    res = differential_pressure_flowmeters.calculate_flow_wetgas_venturi_ReaderHarrisGraham(
        D=venturi['D'],
        d=venturi['d'],
        P1=venturi['P1'],
        dP=venturi['DP'],
        rho_g=venturi['rho_g'],
        rho_l=venturi['rho_l'],
        GVF=gvf,
        H=venturi['H'],
        kappa=venturi['kappa']
    )
    res['GVF'] = gvf
    results[idx] = res
    idx += 1

# Convert results to DataFrame for easier plotting
df = pd.DataFrame(results).T

# Plot Lockhart-Martinelli parameter vs GVF as a smooth line
plt.figure(figsize=(10, 6))
plt.plot(df['GVF'], df['LockhartMartinelli'], linestyle='-', marker=None)
plt.title('Lockhart-Martinelli Parameter vs Gas Volume Fraction')
plt.xlabel('Gas Volume Fraction')
plt.ylabel('Lockhart-Martinelli Parameter')
plt.grid()
plt.show()

# Plot overread vs Lockhart-Martinelli parameter as a smooth line
plt.figure(figsize=(10, 6))
plt.plot(df['LockhartMartinelli'], df['OverRead'], linestyle='-', marker=None)
plt.title('Gas Massflow Overread vs Lockhart-Martinelli Parameter')
plt.xlabel('Lockhart-Martinelli Parameter')
plt.ylabel('Venturi Meter Overreading')
plt.grid()
plt.show()