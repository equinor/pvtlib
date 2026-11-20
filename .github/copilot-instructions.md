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

**tests.yml**: Runs on PRs, pushes to main, nightly, and when called by the release workflow. Jobs: `test` (flake8 + pytest on Ubuntu with Python 3.10-3.14 and on Windows with 3.10 and 3.14), `package` (builds sdist and wheel once, `twine check --strict`, inspects their content, installs each in a clean venv and runs the tests from a copy outside the checkout with `PVTLIB_TEST_INSTALLED_PACKAGE=1` via `tools/test_installed_distributions.sh`; keeps the files, which carry a development version, as artifact `dist` - never published), `examples` (runs every example script and notebook headless) and `coverage`. Checkouts use `fetch-depth: 0` because the version is read from the git tags

**docs.yml**: Builds the Sphinx documentation site with warnings as errors on PRs; publishes it to GitHub Pages (https://equinor.github.io/pvtlib/) from main

**release.yml**: Started by hand only (Actions -> Release -> Run workflow on `main`, input `bump` = patch/minor/major). Jobs: `prepare` (main only, next version from the tags with `tools/release_version.py`, fails if the tag or the PyPI version exists), `test` (calls `tests.yml`), `build` (tags the commit locally, builds sdist + wheel once, checks the version, installs and tests both; artifacts `release-dist` and `release-manifest` with SHA256SUMS), `publish` (environment `pypi`, the only approval; permissions `contents: write` + `id-token: write`, no checkout; verifies the artifacts and PyPI state, creates the tag via the API, uploads with Trusted Publishing - no token - and verifies PyPI holds exactly the manifest files) and `github-release`. No workflow uses a repository secret

All actions are pinned to full commit SHAs; Dependabot (`.github/dependabot.yml`) keeps them up to date.

## Releases
**CRITICAL**: Never write a version in `pyproject.toml` or the code, and never create, move or delete release tags by hand. The version comes from the git tag `MAJOR.MINOR.PATCH` (no prefix) via setuptools-scm, which writes the untracked `pvtlib/_version.py`; `pvtlib.__version__` reads it (`0+unknown` if never installed). Releases are made only with `release.yml`. A change to calculated results is at least a MINOR release. If a release run fails, use "Re-run failed jobs" in the same run - never start a new run for a version that already has files on PyPI. See `docs/releasing.md`.

Supported Python versions: 3.10-3.14 (`requires-python = ">=3.10"`).
