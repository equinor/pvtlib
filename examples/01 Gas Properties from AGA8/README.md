# Gas Properties from AGA8

This example demonstrates how to calculate gas properties using the AGA8 equations of state (GERG-2008 and DETAIL implementations).

> **Note:** AGA8 is only valid for single-phase gas conditions. It does not check for phase state and will produce erroneous results if used in the two-phase or liquid region. Ensure the operating conditions are within the single-phase gas region before using these calculations.

## Description

The example shows how to:
- Set up an AGA8 object for both GERG-2008 and DETAIL equations of state
- Calculate gas properties (density, speed of sound, etc.) from pressure, temperature, and composition
- Compare results between GERG-2008 and DETAIL methods

## Usage

```bash
python gas_properties_from_aga8.py
```

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and prints:
- Mass density from both GERG-2008 and DETAIL methods (kg/m³)
- Speed of sound from both GERG-2008 and DETAIL methods (m/s)
