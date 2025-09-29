<img src="https://github.com/equinor/pvtlib/blob/main/images/pvtlib.png" alt="pvtlib logo" width="600"/>

`pvtlib` is a Python library that provides various tools in the categories of thermodynamics, fluid mechanics, metering and various process equipment. The library includes functions for calculating flow rates, gas properties, and other related calculations.

## Installation

You can install the library using `pip`:

```sh
pip install pvtlib
```

NOTE: The library currently do not support numpy >= 2

## Usage

Here is an example of how to use the library:

```py
from pvtlib.metering import differential_pressure_flowmeters

# Example usage of the calculate_flow_venturi function
result = differential_pressure_flowmeters.calculate_flow_venturi(D=0.1, d=0.05, dP=200, rho1=1000)
print(result)
```

More examples are provided in the examples folder: https://github.com/equinor/pvtlib/tree/main/examples

## Features

- **Thermodynamics**: Thermodynamic functions
- **Fluid Mechanics**: Fluid mechanic functions
- **Metering**: Metering functions
- **aga8**: Equations for calculating gas properties (GERG-2008 and DETAIL) using the Rust port (https://crates.io/crates/aga8) of NIST's AGA8 code (https://github.com/usnistgov/AGA8)
- **Unit converters**: Functions to convert between different units of measure

### Handling of invalid input
This library is used for analyzing large amounts of data, as well as in live applications. In these applications it is desired that the functions return "nan" (using numpy nan) when invalid input are provided, or in case of certain errors (such as "divide by zero" errors). 

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/equinor/pvtlib/blob/main/LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to open an issue or contact the author at chaagen2013@gmail.com.
