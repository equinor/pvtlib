# Gas Density Meter Corrections

This example demonstrates how to apply corrections to gas density meter (GDM) measurements, specifically for Emerson Micro Motion Gas Density Meters (7812 and GDM models).

## Description

Gas density meters measure density by detecting changes in the vibration frequency of a sensing element. The raw measurements need corrections to account for:
- Temperature effects (different from calibration temperature)
- Speed of sound effects (different gas composition from calibration gas)

This example shows the complete workflow:

1. **Calculate uncorrected density** from instrument time period using calibration factors
2. **Apply temperature correction** to account for operating temperature different from calibration temperature
3. **Apply speed of sound correction** to account for process gas properties different from calibration gas (typically nitrogen)

The example demonstrates proper calculation of the calibration gas speed of sound using AGA8, which calculates the speed of sound of nitrogen at the measured density and calibration temperature. 

## Usage

```bash
python gas_density_meter_corrections.py
```

**Note**: This example uses direct imports from `pvtlib.metering.gas_density_meters` to access the gas density meter functions.

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and displays:

- **Step 1**: Uncorrected density from time period (kg/m³)
- **Step 2**: Temperature-corrected density (kg/m³)
- **Step 3**: 
  - Calibration gas (N₂) speed of sound at the measured density (m/s)
  - Process gas speed of sound (m/s)
  - Speed of sound corrected density (kg/m³)

## Key Implementation Details

### Calibration Gas Speed of Sound
- The speed of sound of the calibration gas should be calculated at **the same density** as the measured (uncorrected) density
- Use the calibration temperature (typically 20°C)
- For a GDM calibrated on nitrogen at 20°C, if the meter measures 74.66 kg/m³, then `c_cal` should be the speed of sound of nitrogen at 20°C and 74.66 kg/m³

This example demonstrates this by using `calculate_from_rhoT()` to find the nitrogen properties at the measured density and calibration temperature.

## References

- Micro Motion® Gas Density Meters (GDM): Configuration and Use Manual (2016)
- Micro Motion® Installation and Maintenance Manual - 7812 Gas Density Meter (2012)
- ISO 15970:2014 - Natural gas - Measurement of properties
- Stansfeld, J W (1986) "Velocity of Sound Effect on Gas Density Transducers"
