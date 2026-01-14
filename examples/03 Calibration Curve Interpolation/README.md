# Calibration Curve Interpolation

This example demonstrates how to use linear interpolation to retrieve the corresponding calibration error for a given flowrate from a calibration curve.

## Description

The example shows how to:
- Define a calibration curve with flowrate and calibration error data points
- Use the `linear_interpolation` function from pvtlib utilities to interpolate calibration error at a specific flowrate
- Visualize the calibration curve and interpolated point using matplotlib

This is useful for flowmeter calibration where you have discrete calibration points and need to determine the error at operating flowrates between those points.

## Usage

```bash
python calibration_curve_interpolation.py
```

## Required Packages

- `pvtlib`
- `matplotlib` (for visualization)

## Output

The script:
- Displays a plot showing the calibration curve with the interpolated point highlighted
- Prints the interpolated calibration error at the specified flowrate
