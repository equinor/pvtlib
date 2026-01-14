"""MIT License

Copyright (c) 2026 Christian Hågenvik

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
______________________________________________________________________________
EXAMPLE: Gas Density Meter Corrections

This example demonstrates how to apply corrections to gas density meter (GDM) 
measurements, specifically for Emerson Micro Motion Gas Density Meters (7812 and GDM models).

The example shows the complete workflow:
1. Calculate uncorrected density from instrument time period
2. Apply temperature correction
3. Apply speed of sound correction
4. Calculate volumetric flowrate through the GDM

"""

from pvtlib.metering.gas_density_meters import (
    GDM_uncorr_dens,
    GDM_tempcorr_dens,
    GDM_SOScorr_dens,
    GDM_Q,
    gas_spesific_gravity
)
from pvtlib import AGA8

print("="*70)
print("Gas Density Meter Correction Example")
print("="*70)
print()

# =============================================================================
# STEP 1: Calculate Uncorrected Density from Time Period
# =============================================================================
print("STEP 1: Calculate Uncorrected Density")
print("-" * 70)

# Measured instrument time period
tau = 657.2723  # μs

# Calibration factors from GDM calibration certificate
K0 = -109.934
K1 = -0.0035718
K2 = 0.000432733

# Calculate uncorrected density
Du = GDM_uncorr_dens(
    tau=tau, 
    K0=K0, 
    K1=K1, 
    K2=K2
)

print(f"Measured time period: {tau:.2f} μs")
print(f"Uncorrected density (Du): {Du:.2f} kg/m³")
print()

# =============================================================================
# STEP 2: Apply Temperature Correction
# =============================================================================
print("STEP 2: Apply Temperature Correction")
print("-" * 70)

# Temperature calibration factors
K18 = -1.7973e-05
K19 = 3.4502e-04

# Measured and calibration temperatures
T_measured = 100.0  # °C
T_calibration = 20.0  # °C

# Calculate temperature-corrected density
Dt = GDM_tempcorr_dens(
    Du=Du, 
    K18=K18, 
    K19=K19, 
    T=T_measured, 
    Tcal=T_calibration
)

print(f"Measured temperature: {T_measured:.1f} °C")
print(f"Calibration temperature: {T_calibration:.1f} °C")
print(f"Temperature-corrected density (Dt): {Dt:.2f} kg/m³")
print()

# =============================================================================
# STEP 3: Apply Speed of Sound Correction
# =============================================================================
print("STEP 3: Apply Speed of Sound Correction")
print("-" * 70)

# Define gas composition for process gas
composition = {
    'N2': 1.0,
    'CO2': 2.0,
    'C1': 90.0,
    'C2': 6.4,
    'C3': 0.5,
    'iC4': 0.05,
    'nC4': 0.05
}

# Process conditions
P_process = 50.0  # bara
T_process = 40.0  # °C

# Set up AGA8 for process gas properties
gerg = AGA8('GERG-2008')

# Calculate process gas properties
gas_props = gerg.calculate_from_PT(
    composition=composition,
    pressure=P_process,
    temperature=T_process
)

# Speed of sound for process gas at measured conditions
c_gas = gas_props['w']  # m/s

# Speed of sound for calibration gas (nitrogen at calibration density)
# For this example, the GDM was calibrated on nitrogen at 20°C
# We need the speed of sound of nitrogen at the same density as the measured density

# Calculate speed of sound for N2 at the corresponding density
N2_props = gerg.calculate_from_rhoT(
    composition={'N2': 100.0},
    mass_density=Du, # Use uncorrected density (as this is directly from the measured time period)
    temperature=20.0, # calibration temperature
    temperature_unit='C'
)

# Speed of sound of calibration gas at Du and 20°C (calibration temperature)
c_cal = N2_props['w']  # m/s

# Speed of sound constant (for Micro Motion GDM)
K = 2.1e4

# Calculate speed of sound corrected density
Dvos = GDM_SOScorr_dens(
    rho=Dt, 
    tau=tau, 
    c_cal=c_cal, 
    c_gas=c_gas, 
    K=K
)

print(f"Calibration gas speed of sound: {c_cal:.2f} m/s")
print(f"Process gas speed of sound: {c_gas:.2f} m/s")
print(f"Speed of sound corrected density (Dvos): {Dvos:.2f} kg/m³")
print()