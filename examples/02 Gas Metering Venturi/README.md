# Gas Metering Venturi

This example demonstrates how to calculate gas flowrate through a venturi meter given its geometry and measured differential pressure.

## Description

The example shows how to:
- Calculate gas properties using the GERG-2008 equation of state
- Calculate venturi beta ratio from geometry
- Calculate expansibility factor for the venturi
- Calculate mass flow, volume flow, and velocity through the venturi

Gas properties are calculated using the GERG-2008 equation of state, which provides accurate density and isentropic exponent values needed for the venturi flow calculations.

## Usage

```bash
python gas_metering_venturi.py
```

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and prints:
- Gas mass density (kg/m³)
- Venturi beta ratio
- Venturi expansibility factor
- Mass flowrate (kg/h)
- Volume flowrate (m³/h)
- Velocity (m/s)
