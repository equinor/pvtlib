# Wetgas Venturi Overread - Reader Harris

This example demonstrates the calculation of overread correction for wet gas venturi meters using the Reader-Harris/Graham correlation, with sensitivity analysis on gas density and gas volume fraction.

## Description

The example shows how to:
- Calculate wetgas venturi flowrates using the Reader-Harris/Graham correlation
- Perform sensitivity analysis varying gas volume fraction (GVF) and gas density
- Visualize the Lockhart-Martinelli parameter and overread as functions of GVF and gas density

**Wet gas**: A gas stream containing small amounts of liquid (typically GVF > 0.95). When measured with a differential pressure meter designed for single-phase gas, the liquid phase causes an overread in the indicated gas flowrate.

**Reader-Harris/Graham correlation**: An industry-standard method for correcting venturi meter readings in wet gas conditions.

## Usage

```bash
python wetgas_venturi_overread_ReaderHarris.py
```

## Required Packages

- `pvtlib`
- `numpy` (for creating value ranges)
- `pandas` (for data handling)
- `matplotlib` (for visualization)

## Output

The script generates two plots:
1. Lockhart-Martinelli parameter vs. Gas Volume Fraction for different gas densities
2. Gas mass flow overread vs. Lockhart-Martinelli parameter for different gas densities

These plots help understand how the overread correction varies with operating conditions.
