# Gas Properties from AGA8

This example demonstrates how to calculate gas properties using the AGA8 equation of state (GERG-2008 and DETAIL implementations).

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
