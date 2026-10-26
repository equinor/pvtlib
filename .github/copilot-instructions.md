# AI Agent Instructions for pvtlib

## What is this?
Python library for oil & gas thermodynamics, fluid mechanics, and metering. Wraps Rust-based AGA8 for gas property calculations.

## Instructions for AI Use in Code Generation

1. **Correctness first**: Calculations must be mathematically, physically and numerically correct. Code that runs is not proof that the result is right. Treat calculations as a basis for decisions with safety and cost consequences.
2. **Units must be explicit**: Document the unit of every input and output. Never assume units, and never convert, scale or adjust values silently. Ask when a unit is unclear.
3. **Do not guess**: Do not invent constants, correlations, assumptions or acceptance criteria. Stop and ask when something is unclear. Respect and document the validity range of a model.
4. **Verified references only**: Cite only standards, papers and equation numbers you have actually read. State clearly when something is unverified.
5. **Investigate failures, do not hide them**: A failing test or function has a cause. Find it. Never weaken tolerances, criteria or tests to make something pass. Present the root cause and the options before making impactful changes.
6. **Simple, debuggable code**: Small, explicit functions. Visible formulas, descriptive variable names, no unnecessary abstraction, indirection or hidden state. Intermediate values must be easy to inspect in a debugger.
7. **Tests with real expected values**: Plain pytest functions with exact expected values from an independent source. No weak tests that only check that a result exists, is positive or looks reasonable.
8. **Test several conditions**: Normal cases, several representative points, boundary values, zero, negative values and invalid input.
9. **Stay within the task**: Do only what was asked. Do not rename, move, delete or refactor existing code, tests or data without saying so and getting approval first.
10. **Short, verifiable reporting**: State what was changed, the engineering reasoning, the assumptions made, how it was verified, and what remains. Keep it short enough to actually be read.

## Critical Patterns

**Error handling**: Two distinct approaches depending on error type:
- Return `np.nan` for real-world invalid measurements (negative pressures, divide by zero, non-physical values) - prevents crashes during large-scale analysis
- Raise exceptions (`ValueError`, etc.) for programming errors where the user makes a mistake (wrong units, malformed inputs, incorrect function usage)

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

**validate-version.yml**: Validates `pyproject.toml` version - runs on releases (fails if mismatch), push/PR (warns only)

**build-and-distribute-test.yml**: Tests the build & distribution process on pre-releases (validates version, builds package, runs `twine check` - does NOT publish to PyPI)

**build-and-distribute.yml**: Production release - waits for version validation, then publishes to PyPI on full releases

## Releases
**CRITICAL**: Update `pyproject.toml` version before creating GitHub releases - workflows validate version match before PyPI publish
