# Gas Mixing Calculation

This example demonstrates how to calculate the resulting gas composition when mixing multiple streams with different compositions, pressures, and temperatures.

## Description

The example shows how to:
- Calculate gas density using the AGA8 GERG-2008 equation of state
- Convert volumetric flowrate to mass flowrate using calculated density
- Mix multiple gas streams with different compositions
- Perform subtraction operations (e.g., removing a stream from a mixture)
- Calculate the final composition of the mixed stream

## Scenario

Three gas streams are involved in this process:
- **Gas 1** and **Gas 2** are produced into a single mixing point
- A reactor removes **Gas 3** from this mixture
- **Stream 4** (output) = Gas 1 + Gas 2 - Gas 3

Each stream is measured by an ultrasonic flowmeter providing volumetric flowrate Q [m³/h].

## Usage

Open the Jupyter notebook:

```bash
jupyter notebook gas_mixing_calculation.ipynb
```

## Required Packages

- `pvtlib`
- `pandas`
- `numpy`

## Input Data

| Parameter | Gas 1 | Gas 2 | Gas 3 |
|-----------|-------|-------|-------|
| Q [m³/h] | 5000 | 3000 | 500 |
| P [bara] | 150 | 130 | 30 |
| T [°C] | 50 | 40 | 30 |
| **Composition [mole %]** | | | |
| N2 | 1 | 10 | 10 |
| CO2 | 2 | 5 | 60 |
| C1 | 90 | 81 | 30 |
| C2 | 6 | 4 | - |
| C3 | 0.9 | - | - |
| iC4 | 0.05 | - | - |
| nC4 | 0.05 | - | - |

## Output

The notebook calculates and displays:
- Gas density for each stream using GERG-2008 [kg/m³]
- Mass flowrate for each stream [kg/h]
- Final composition of Stream 4 [mole %]
- Total mass flowrate of Stream 4 [kg/h]

## Key Features

- Uses the `AGA8.mix()` function to handle gas mixing calculations
- Supports negative mass values for subtraction operations
- Handles different gas compositions with varying number of components
- Provides formatted output tables for easy interpretation
