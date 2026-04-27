<img src="https://raw.githubusercontent.com/equinor/pvtlib/main/images/pvtlib_klab.png" alt="pvtlib logo" width="600"/>

[![PyPI version](https://img.shields.io/pypi/v/pvtlib)](https://pypi.org/project/pvtlib/)
[![Python versions](https://img.shields.io/pypi/pyversions/pvtlib)](https://pypi.org/project/pvtlib/)
[![Tests](https://github.com/equinor/pvtlib/actions/workflows/python-package-run-tests.yml/badge.svg)](https://github.com/equinor/pvtlib/actions/workflows/python-package-run-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`pvtlib` is a Python librarythat provides various tools in the categories of thermodynamics, fluid mechanics, metering and various process equipment. The library includes functions for calculating flow rates, gas properties, and other related calculations.

## Installation

You can install the library using `pip`:

```sh
pip install pvtlib
```

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
- **aga8**: Equations for calculating gas properties (GERG-2008 and DETAIL) using the Rust port (https://crates.io/crates/aga8) of NIST's AGA8 code (https://github.com/usnistgov/AGA8). **Note: AGA8 is only valid for single-phase gas conditions. It does not check for phase state and will produce erroneous results in the two-phase or liquid region.**
- **Unit converters**: Functions to convert between different units of measure
- **Equipment**:
  - **Compressors**: Compressor performance calculations (e.g. polytropic exponent, polytropic head and efficiency)
  - **Separators**: Separator/scrubber sizing functions (e.g. K-value calculations)
  - **Valves**: Valve flow calculations (e.g. Kv/Cv flow factor)

### Handling of invalid input
This library is used for analyzing large amounts of data, as well as in live applications. In these applications it is desired that the functions return "nan" (using numpy nan) when invalid input are provided, or in case of certain errors (such as "divide by zero" errors). 

## Running Tests

Tests are located in the `tests/` folder and use [pytest](https://docs.pytest.org/). Install it before running:

```sh
pip install pytest
```

Then run the tests from the project root:

```sh
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/equinor/pvtlib/blob/main/LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to open an issue or contact the author at chaagen2013@gmail.com.
