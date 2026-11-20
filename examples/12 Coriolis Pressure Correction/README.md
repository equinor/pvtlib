# Coriolis Pressure Correction

This example corrects the accumulated mass of a Coriolis flowmeter for the process-pressure effect,
using a calibration run of an Emerson Micro Motion CMF300H at an accredited calibration facility.

## Description

The notebook shows how to:
- Convert the process-pressure effect from the product data sheet (PDS) to the correction factor
  `PCm`, which has the opposite sign
- Correct the measured accumulated mass with
  `pvtlib.metering.coriolis_flowmeters.coriolis_massflow_corr_pres()`
- Calculate the error relative to the reference with and without the pressure correction

## Equations

Mass-flow pressure correction:

$$m_{corr} = m_{meas}\left(1 + \frac{PCm}{100}(P_{act}-P_{cal})\right)$$

Error relative to the reference:

$$\text{error}~[\%] = 100\cdot\frac{m - m_{ref}}{m_{ref}}$$

## Input Data

| Parameter | Value |
|-----------|-------|
| Meter | Emerson Micro Motion CMF300H |
| Pressure during the calibration run, `P_act` | 60 bara |
| Factory calibration pressure of the meter, `P_cal` | 2.55 bara |
| Reference accumulated mass | 4120.487 kg |
| Coriolis accumulated mass (pressure compensation disabled) | 4105.007 kg |
| Flow rate during the run | 82 tonnes/h |
| Process-pressure effect from the PDS | -0.006 % of rate per bar |
| Correction factor `PCm` | +0.006 %/bar |

## Usage

Open the Jupyter notebook:

```bash
jupyter notebook coriolis_pressure_correction_example.ipynb
```

## Required Packages

- `pvtlib`
- `pandas`

## Output

The notebook shows a table with the accumulated mass [kg] and the error relative to the reference
[%], without and with the pressure correction.
