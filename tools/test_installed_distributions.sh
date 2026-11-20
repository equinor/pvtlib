#!/usr/bin/env bash
# Installs the wheel and the sdist in dist/ into two clean virtual environments and runs the test
# suite against each installed package. Used by the "package" job of tests.yml and by the "build"
# job of release.yml, on Linux runners.
#
# Usage: tools/test_installed_distributions.sh DIST_DIR WORK_DIR [EXPECTED_VERSION]
#
#   DIST_DIR          folder with exactly one pvtlib-*.whl and one pvtlib-*.tar.gz
#   WORK_DIR          empty folder outside the checkout for the virtual environments and test copies
#   EXPECTED_VERSION  if given, pvtlib.__version__ and the installed metadata must equal it
#
# The tests run from a copy outside the checkout with --import-mode=importlib, so the pvtlib folder
# of the checkout is never on sys.path. PVTLIB_TEST_INSTALLED_PACKAGE=1 makes tests/conftest.py
# stop the session unless pvtlib is imported from that environment's site-packages. The sdist is
# unpacked into a folder without .git before it is installed, so setuptools-scm reads the version
# from the sdist's PKG-INFO, as it does for a user installing the sdist from PyPI.

set -euo pipefail

dist_dir=$(cd "$1" && pwd)
work_dir=$(cd "$2" && pwd)
expected_version="${3:-}"
repository_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

export PVTLIB_TEST_INSTALLED_PACKAGE=1

test_installed() {
  local label="$1"
  local requirement="$2"
  local venv="${work_dir}/venv-${label}"
  local tests_copy="${work_dir}/tests-${label}"
  echo "::group::Test the installed ${label}: ${requirement}"
  python -m venv "${venv}"
  "${venv}/bin/python" -m pip install --upgrade pip
  "${venv}/bin/python" -m pip install "${requirement}"
  mkdir -p "${tests_copy}"
  (cd "${repository_root}" && cp -r tests tools docs examples README.md LICENSE "${tests_copy}/")
  if [ -n "${expected_version}" ]; then
    (cd "${tests_copy}" && EXPECTED_VERSION="${expected_version}" "${venv}/bin/python" -P - <<'PY'
import importlib.metadata
import os

import pvtlib

expected = os.environ["EXPECTED_VERSION"]
print("pvtlib", pvtlib.__version__, "imported from", pvtlib.__file__)
assert pvtlib.__version__ == expected, (pvtlib.__version__, expected)
assert importlib.metadata.version("pvtlib") == expected, (importlib.metadata.version("pvtlib"), expected)
PY
    )
  fi
  (cd "${tests_copy}" && "${venv}/bin/python" -m pytest --import-mode=importlib -p no:cacheprovider tests)
  echo "::endgroup::"
}

wheels=("${dist_dir}"/pvtlib-*.whl)
sdists=("${dist_dir}"/pvtlib-*.tar.gz)
if [ "${#wheels[@]}" -ne 1 ] || [ ! -f "${wheels[0]}" ] || [ "${#sdists[@]}" -ne 1 ] || [ ! -f "${sdists[0]}" ]; then
  echo "::error::Expected exactly one pvtlib wheel and one pvtlib sdist in ${dist_dir}"
  ls -l "${dist_dir}"
  exit 1
fi

test_installed wheel "${wheels[0]}[test]"

mkdir -p "${work_dir}/sdist"
tar -xzf "${sdists[0]}" -C "${work_dir}/sdist"
sdist_dirs=("${work_dir}"/sdist/pvtlib-*)
if [ "${#sdist_dirs[@]}" -ne 1 ] || [ ! -d "${sdist_dirs[0]}" ]; then
  echo "::error::Expected one pvtlib-* folder in the unpacked sdist"
  exit 1
fi
if [ -e "${sdist_dirs[0]}/.git" ]; then
  echo "::error::The unpacked sdist contains .git"
  exit 1
fi
test_installed sdist "${sdist_dirs[0]}[test]"
