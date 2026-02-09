# AI Agent Instructions for pvtlib

## What is this?
Python library for oil & gas thermodynamics, fluid mechanics, and metering. Wraps Rust-based AGA8 for gas property calculations.

## Critical Patterns

**Error handling**: Return `np.nan` for invalid inputs, never raise exceptions (used in large-scale analysis)

**Function returns**: Always return dictionaries with descriptive keys, never tuples:
```python
return {'MassFlow': mass_flow, 'VolFlow': vol_flow, 'Velocity': velocity}
```

**AGA8 setup**: Must instantiate before use:
```python
gerg = pvtlib.AGA8('GERG-2008')  # Do once
properties = gerg.calculate_from_PT(composition, pressure, temperature)
```

**Documentation**: 
- MIT license header in all files (copy from existing)
- NumPy-style docstrings with ISO standard references

**Testing**: Every function must have at least one unit test in `tests/`

## Workflows

**python-package-run-tests.yml**: Runs pytest on push/PR for Python 3.9-3.13

**validate-version.yml**: Validates `setup.py` version - runs on releases (fails if mismatch), push/PR (warns only)

**build-and-distribute-test.yml**: Tests the build & distribution process on pre-releases (validates version, builds package, runs `twine check` - does NOT publish to PyPI)

**build-and-distribute.yml**: Production release - waits for version validation, then publishes to PyPI on full releases

## Releases
**CRITICAL**: Update `setup.py` version before creating GitHub releases - workflows validate version match before PyPI publish
