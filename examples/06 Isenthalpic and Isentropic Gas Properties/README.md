# Isenthalpic and Isentropic Gas Properties

This example demonstrates how to calculate gas properties during isenthalpic (constant enthalpy) and isentropic (constant entropy) processes.

## Description

The example shows how to:
- Calculate gas properties at initial conditions using `calculate_from_PT` (pressure and temperature)
- Calculate temperature after an isenthalpic expansion using `calculate_from_PH` (pressure and enthalpy)
- Calculate temperature after an isentropic process using `calculate_from_PS` (pressure and entropy)

**Isenthalpic process**: Occurs during throttling (e.g., flow through a valve or restriction) where no heat is exchanged and no work is done.

**Isentropic process**: An idealized reversible adiabatic process (no heat transfer, no entropy change) often used for analyzing compressors and turbines.

## Usage

```bash
python isenthalpic_and_isentropic_gas_properties.py
```

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and prints:
- Temperature after isenthalpic expansion (°C)
- Gas density and speed of sound after isenthalpic expansion
- Temperature after isentropic process (°C)
