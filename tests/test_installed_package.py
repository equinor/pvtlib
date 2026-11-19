"""MIT License

Copyright (c) 2025 Christian Hågenvik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""Tests for the import-location check in tests/conftest.py that the release workflow relies on."""

import importlib.util
from pathlib import Path


def _load_conftest():
    # Loaded by path, because tests/ is also run as a copy outside the checkout with
    # --import-mode=importlib, where "tests.conftest" is not importable.
    spec = importlib.util.spec_from_file_location("pvtlib_tests_conftest", Path(__file__).with_name("conftest.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


conftest = _load_conftest()

SITE_PACKAGES = Path("/venv/lib/python3.13/site-packages")
WORKSPACE = Path("/home/runner/work/pvtlib/pvtlib")


def test_installed_package_outside_checkout_has_no_problems():
    package_file = SITE_PACKAGES / "pvtlib" / "__init__.py"
    assert conftest.installed_package_problems(package_file, [SITE_PACKAGES], WORKSPACE) == []


def test_package_in_checkout_is_reported():
    package_file = WORKSPACE / "pvtlib" / "__init__.py"
    problems = conftest.installed_package_problems(package_file, [SITE_PACKAGES], WORKSPACE)
    assert len(problems) == 2
    assert "not in the site-packages" in problems[0]
    assert "inside the checkout" in problems[1]


def test_package_outside_site_packages_is_reported_without_workspace():
    package_file = Path("/somewhere/else/pvtlib/__init__.py")
    problems = conftest.installed_package_problems(package_file, [SITE_PACKAGES], None)
    assert len(problems) == 1
    assert "not in the site-packages" in problems[0]


def test_site_packages_inside_workspace_is_reported():
    # A virtual environment created inside the checkout does not prove the installed files are used.
    site_packages_in_workspace = WORKSPACE / ".venv" / "lib" / "python3.13" / "site-packages"
    package_file = site_packages_in_workspace / "pvtlib" / "__init__.py"
    problems = conftest.installed_package_problems(package_file, [site_packages_in_workspace], WORKSPACE)
    assert len(problems) == 1
    assert "inside the checkout" in problems[0]
