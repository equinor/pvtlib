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

"""Tests for the package version, pvtlib.__version__.

The version is set by hand in pyproject.toml (see docs/releasing.md). pvtlib.__version__ reads it
from the metadata of the installed package, so the version a calculation reports is the version
pip installed.
"""

import importlib.metadata

import pvtlib


def test_version_matches_installed_package_metadata():
    # Fails if the code being tested is not the code that was installed, e.g. a source tree that
    # was never installed ("0+unknown"), or an older editable install. The fix is to reinstall:
    # pip install -e .
    assert pvtlib.__version__ == importlib.metadata.version("pvtlib")


def test_version_is_not_the_unknown_fallback():
    assert pvtlib.__version__ != "0+unknown"
