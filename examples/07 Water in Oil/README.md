# Water in Oil

This example demonstrates how to handle water contamination in oil metering systems using density measurements.

## Description

The example shows three common calculations:

1. **Water cut from mixed density**: Calculate the volume percentage of water in oil from a measured mixed density
2. **Weight percent of water**: Convert volume percent to weight (mass) percent
3. **Corrected oil density**: Calculate the true oil density when water content is known

These calculations are important for oil metering stations where:
- A Coriolis meter measures the density of the oil-water mixture
- A water cut meter measures the water fraction
- You need to correct flowrates and densities for accurate custody transfer

## Usage

```bash
python water_in_oil.py
```

## Required Packages

- `pvtlib` (only)

## Output

The script calculates and prints:
- Water cut (volume %)
- Water weight percent (mass %)
- Corrected oil density without water contamination (kg/m³)
