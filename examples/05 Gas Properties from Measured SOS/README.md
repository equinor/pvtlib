# Gas Properties from Measured Speed of Sound

This example demonstrates how to calculate gas properties (density, molar mass, compressibility factor) from a measured speed of sound value.

## Description

The example shows two approaches:
1. **Using the convenience method**: `properties_from_sos_kappa()` calculates all properties in one call
2. **Using individual functions**: Separate calls to calculate density, molar mass, and compressibility factor from speed of sound

This is useful when you have a speed-of-sound meter (sonic meter) and want to derive other gas properties from the measured speed of sound. The method uses the gas composition and operating conditions along with the measured speed of sound to back-calculate properties.

## Usage

```bash
python gas_properties_from_measured_sos.py
```

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and prints:
- Density calculated from measured speed of sound (kg/m³)
- Molar mass calculated from measured speed of sound (kg/kmol)
- Compressibility factor calculated from measured speed of sound

Results are shown using both the convenience method and individual function calls to demonstrate equivalence.
