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

"""Check, inside the pytest session, which pvtlib the tests are running against.

The release workflow installs the built wheel and the sdist into clean virtual environments and
runs a copy of these tests against them. That only proves something if the tests import the
installed package and not a pvtlib folder from the repository checkout. With the environment
variable PVTLIB_TEST_INSTALLED_PACKAGE=1 the session stops at the first test unless pvtlib is
imported from the site-packages of the Python running pytest, outside the checkout
(GITHUB_WORKSPACE). Without the variable, as in normal local runs, nothing is checked.
"""

import importlib.metadata
import os
import sysconfig
from pathlib import Path

import pytest

INSTALLED_PACKAGE_VARIABLE = "PVTLIB_TEST_INSTALLED_PACKAGE"


def installed_package_problems(package_file, site_packages_dirs, workspace):
    """List the reasons a pvtlib import location is not an installed package.

    Parameters
    ----------
    package_file : pathlib.Path
        Resolved path of ``pvtlib.__file__``.
    site_packages_dirs : list of pathlib.Path
        Resolved site-packages folders of the running Python (purelib and platlib).
    workspace : pathlib.Path or None
        Resolved repository checkout (GITHUB_WORKSPACE), or None when it is not known.

    Returns
    -------
    list of str
        Empty when the package is inside one of the site-packages folders and outside the checkout.
    """
    problems = []
    if not any(package_file.is_relative_to(folder) for folder in site_packages_dirs):
        problems.append(f"pvtlib is imported from {package_file}, which is not in the site-packages "
                        f"of this Python ({', '.join(str(folder) for folder in site_packages_dirs)})")
    if workspace is not None and package_file.is_relative_to(workspace):
        problems.append(f"pvtlib is imported from {package_file}, inside the checkout {workspace}")
    return problems


def pytest_report_header(config):
    import pvtlib
    return f"pvtlib {pvtlib.__version__} imported from {Path(pvtlib.__file__).resolve()}"


@pytest.fixture(scope="session", autouse=True)
def _check_installed_package():
    """Stop the session before the first test when PVTLIB_TEST_INSTALLED_PACKAGE=1 and pvtlib is
    not imported from the installed package. A session fixture, rather than a session-start hook,
    runs however pytest is started and wherever this conftest.py is found."""
    if os.environ.get(INSTALLED_PACKAGE_VARIABLE) != "1":
        return
    import pvtlib

    package_file = Path(pvtlib.__file__).resolve()
    site_packages_dirs = sorted({Path(sysconfig.get_paths()[key]).resolve() for key in ("purelib", "platlib")})
    workspace = Path(os.environ["GITHUB_WORKSPACE"]).resolve() if os.environ.get("GITHUB_WORKSPACE") else None
    problems = installed_package_problems(package_file, site_packages_dirs, workspace)
    installed_version = importlib.metadata.version("pvtlib")
    if pvtlib.__version__ != installed_version:
        problems.append(f"pvtlib.__version__ {pvtlib.__version__} differs from the installed metadata "
                        f"{installed_version}")
    if problems:
        pytest.exit(f"{INSTALLED_PACKAGE_VARIABLE}=1, but: " + "; ".join(problems), returncode=1)
    print(f"\n{INSTALLED_PACKAGE_VARIABLE}=1: pvtlib {pvtlib.__version__} is imported from {package_file}")
