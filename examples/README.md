# Examples

This folder provides calculation examples utilizing the different methods in the pvtlib library. 

## Installation

To use these examples, pvtlib must be installed:

```sh
pip install pvtlib
```

Some examples may require additional packages (matplotlib, numpy, pandas) - see individual example READMEs for details.

## Example Overview

### 01 Gas Properties from AGA8
Calculate gas properties (density, speed of sound) using AGA8 equations of state (GERG-2008 and DETAIL). Compare results between different EOS implementations.

**Required packages**: pvtlib only

### 02 Gas Metering Venturi
Calculate gas flowrate through a venturi meter from geometry and differential pressure measurements. Includes calculation of beta ratio, expansibility factor, and flow properties.

**Required packages**: pvtlib only

### 03 Calibration Curve Interpolation
Interpolate calibration error from discrete calibration points for flowmeters. Includes visualization of calibration curves.

**Required packages**: pvtlib, matplotlib

### 04 Critical Velocity for Homogeneous Mixture Oil Water
Calculate the critical velocity needed to maintain homogeneous water-in-oil dispersion in horizontal and vertical pipes. Important for multiphase flow measurement.

**Required packages**: pvtlib only

### 05 Gas Properties from Measured SOS
Calculate gas properties (density, molar mass, compressibility factor) from measured speed of sound values. Demonstrates both convenience methods and individual calculation functions.

**Required packages**: pvtlib only

### 06 Isenthalpic and Isentropic Gas Properties
Calculate gas properties during isenthalpic (throttling) and isentropic (reversible adiabatic) processes. Useful for analyzing valves, compressors, and turbines.

**Required packages**: pvtlib only

### 07 Water in Oil
Handle water contamination in oil metering systems. Calculate water cut from mixed density, convert between volume and mass percentages, and correct oil density for water content.

**Required packages**: pvtlib only

### 08 Wetgas Venturi Overread Reader Harris
Calculate overread correction for wet gas venturi meters using the Reader-Harris/Graham correlation. Includes sensitivity analysis and visualization of Lockhart-Martinelli parameter and overread.

**Required packages**: pvtlib, numpy, pandas, matplotlib

### 09 Gas Density Meter Corrections
Apply corrections to gas density meter (GDM) measurements for Emerson Micro Motion Gas Density Meters. Demonstrates temperature correction, speed of sound correction, and flowrate calculation. Includes examples at different density ranges.

**Required packages**: pvtlib only

## Usage

Each example is contained in its own numbered folder with:
- The Python script implementing the example
- A README.md file with detailed description and requirements

Navigate to the desired example folder and run the Python script:

```sh
cd "01 Gas Properties from AGA8"
python gas_properties_from_aga8.py
```

## Contributing

If you have suggestions for new examples or improvements to existing ones, please open an issue or submit a pull request.