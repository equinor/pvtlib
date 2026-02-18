# Example 11: Compressor Performance Calculations

This example demonstrates how to calculate various compressor performance parameters using pvtlib. The example combines gas property calculations from AGA8 (GERG-2008) with compressor performance functions.

## Overview

The example calculates compressor performance metrics for a natural gas compression process with:
- Suction conditions: 60 bara, 40°C
- Discharge conditions: 75 bara, 60°C
- Single impeller centrifugal compressor
- Compressor speed: 3600 rpm
- Impeller diameter: 0.4 m
- Inlet volumetric flow: 2.5 m³/s

## Calculations Performed

### Gas Properties
Using AGA8 GERG-2008 equation of state:
- Mass density at suction and discharge conditions
- Molar mass
- Compressibility factor
- Enthalpy (converted to mass-specific basis)

### Compressor Performance Parameters
1. **Polytropic exponent (n)** - Characterizes the compression process
2. **Polytropic head** - The ideal head for the polytropic process [kJ/kg]
3. **Enthalpy rise (Δh)** - Actual energy added to the gas [kJ/kg]
4. **Polytropic efficiency** - Ratio of polytropic head to enthalpy rise
5. **Impeller tip speed** - Tangential velocity at impeller outer diameter [m/s]
6. **Sigma U²** - Sum of squared tip speeds for all impellers [J/kg]
7. **Polytropic head coefficient (μ)** - Dimensionless head parameter
8. **Work coefficient (λ)** - Dimensionless work parameter
9. **Flow coefficient** - Dimensionless flow parameter (MAN and ISO 5389 definitions)
10. **Mass flow rate** - Gas mass flow through compressor [kg/s]
11. **Compressor power** - Total power consumption [kW]

## Usage

```python
python compressor_performance_calculations.py
```

## Key Functions Used

- `pvtlib.AGA8()` - Initialize AGA8 equation of state
- `pvtlib.equipment.compressors.poly_exp()` - Calculate polytropic exponent
- `pvtlib.equipment.compressors.poly_head()` - Calculate polytropic head
- `pvtlib.equipment.compressors.poly_eff()` - Calculate polytropic efficiency
- `pvtlib.equipment.compressors.dh()` - Calculate enthalpy rise
- `pvtlib.equipment.compressors.impeller_tang_vel()` - Calculate tip speed
- `pvtlib.equipment.compressors.sigma_u_squared()` - Calculate sigma U²
- `pvtlib.equipment.compressors.poly_head_coeff()` - Calculate head coefficient
- `pvtlib.equipment.compressors.work_coefficient()` - Calculate work coefficient
- `pvtlib.equipment.compressors.flow_coeff()` - Calculate flow coefficient

## Output

The script provides detailed output including:
- Gas properties at suction and discharge conditions
- All calculated compressor performance parameters
- Performance coefficients in dimensionless form
- Mass flow rate and power consumption
