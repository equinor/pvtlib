# Releasing pvtlib

pvtlib is published to [PyPI](https://pypi.org/project/pvtlib/) from a GitHub release. The
version is set by hand in `pyproject.toml`; there is no automatic version bump.

## Version numbers

Versions are `MAJOR.MINOR.PATCH` without a prefix, for example `1.16.1`. The git tag of a release is
the same string. `pvtlib.__version__` reports the version of the installed package, read from its
package metadata:

| Installed from | `pvtlib.__version__` |
|---|---|
| PyPI, a wheel or an sdist | the version in `pyproject.toml` when it was built |
| `pip install -e .` | the version in `pyproject.toml` when it was installed |
| a source tree that was never installed | `0+unknown` |

After changing the version in `pyproject.toml`, run `pip install -e .` again in an editable
environment; `tests/test_version.py` fails until the installed metadata matches.

## Making a release

1. In a pull request, change `version` in `pyproject.toml` and merge it into `main` when the checks
   are green.
2. On GitHub, create a release from `main` with a new tag equal to that version (for example
   `1.17.0`) and publish it.
3. Publishing the release starts the workflow
   [`build-and-distribute.yml`](../.github/workflows/build-and-distribute.yml), which runs on the
   tagged commit:
   1. checks that the version in `pyproject.toml` equals the tag (a leading `v` is ignored) and stops
      if it does not,
   2. runs the complete test workflow, [`tests.yml`](../.github/workflows/tests.yml). Its `package`
      job builds the sdist and the wheel once, checks them with `twine check --strict`, inspects
      their content, installs each in a clean virtual environment and runs the test suite against
      the installed package (from a copy of `tests/` outside the checkout, with a check inside the
      pytest session that `pvtlib` is imported from that environment),
   3. checks that the tested files are exactly `pvtlib-<version>.tar.gz` and
      `pvtlib-<version>-py3-none-any.whl`, and lists their SHA-256 in the run summary,
   4. uploads exactly those files to PyPI with `twine`. Nothing is rebuilt between testing and
      upload. Only this last job has access to the PyPI token.

If any step before the upload fails, nothing is published. Fix the cause, then delete the GitHub
release and its tag, or publish a new version. A version that has been uploaded to PyPI can never
be uploaded again, even if it is deleted there, so a mistake in a published version is corrected
with a new version.

## Python versions

pvtlib supports the Python versions listed in `requires-python` and the classifiers in
`pyproject.toml`. The test workflow runs on all of them. When a Python version is dropped, pip on
that Python keeps installing the last release that supported it.
