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

"""Tests for tools/release_version.py, which works out the next release version from the git tags.

The release workflow relies on this to name the release, so a wrong answer would publish a release
under the wrong version. Tag lists are given explicitly in each test.
"""

import importlib.util
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

# The tags of equinor/pvtlib when the release workflow was introduced (git ls-remote --tags origin,
# 2026-11-20). All are lightweight and unprefixed. There is no 1.12.0 and no 1.16.0.
PVTLIB_TAGS = [
    "1.1.5", "1.1.6", "1.1.7", "1.10.0", "1.11.0", "1.13.0", "1.14.0", "1.14.1", "1.14.2",
    "1.14.3", "1.14.4", "1.14.5", "1.15.0", "1.15.1", "1.16.1", "1.2.0", "1.3.0", "1.4.0",
    "1.5.0", "1.6.0", "1.7.0", "1.7.1", "1.7.2", "1.8.1", "1.8.2", "1.9.0", "1.9.1",
]


def _load_release_version():
    spec = importlib.util.spec_from_file_location(
        "release_version", REPOSITORY_ROOT / "tools" / "release_version.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release_version = _load_release_version()


# --- the real pvtlib tags --------------------------------------------------------------------------

def test_latest_release_of_pvtlib_tags():
    assert release_version.latest_release(PVTLIB_TAGS) == (1, 16, 1)


def test_next_version_from_pvtlib_tags():
    latest = release_version.latest_release(PVTLIB_TAGS)
    assert release_version.next_version(latest, "patch") == (1, 16, 2)
    assert release_version.next_version(latest, "minor") == (1, 17, 0)
    assert release_version.next_version(latest, "major") == (2, 0, 0)


def test_main_with_pvtlib_tags(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", _Stdin("\n".join(PVTLIB_TAGS) + "\n"))
    assert release_version.main(["--bump", "minor"]) == 0
    assert capsys.readouterr().out == "1.17.0\n"


# --- parse_release_tag -----------------------------------------------------------------------------

def test_parse_release_tag():
    assert release_version.parse_release_tag("1.16.1") == (1, 16, 1)
    assert release_version.parse_release_tag("0.1.0") == (0, 1, 0)
    assert release_version.parse_release_tag("0.0.0") == (0, 0, 0)
    assert release_version.parse_release_tag("10.20.300") == (10, 20, 300)


def test_parse_release_tag_with_prefix():
    assert release_version.parse_release_tag("v1.2.5", prefix="v") == (1, 2, 5)


@pytest.mark.parametrize("tag", [
    "v1.2.5",         # prefix, but pvtlib tags have none
    "1.2",            # missing patch
    "1.2.5.1",        # four parts
    "1.2.5rc1",       # pre-release
    "1.2.5-beta",     # pre-release
    "1.2.5.post1",    # post-release
    "01.2.5",         # leading zero
    "1.02.5",         # leading zero
    "1.2.-5",         # negative
    "1.2.5 ",         # trailing space
    "",
])
def test_parse_release_tag_rejects_anything_but_major_minor_patch(tag):
    with pytest.raises(ValueError):
        release_version.parse_release_tag(tag)


@pytest.mark.parametrize("tag", ["1.2.5", "V1.2.5", "v1.2", "vv1.2.5"])
def test_parse_release_tag_with_prefix_rejects_other_forms(tag):
    with pytest.raises(ValueError):
        release_version.parse_release_tag(tag, prefix="v")


# --- latest_release --------------------------------------------------------------------------------

def test_latest_release_with_no_tags_is_zero():
    assert release_version.latest_release([]) == (0, 0, 0)
    assert release_version.latest_release(["", "   "]) == (0, 0, 0)


def test_latest_release_compares_numerically_not_as_text():
    assert release_version.latest_release(["1.9.0", "1.10.0", "1.2.0"]) == (1, 10, 0)
    assert release_version.latest_release(["0.1.9", "0.1.10"]) == (0, 1, 10)
    assert release_version.latest_release(["9.0.0", "10.0.0"]) == (10, 0, 0)


def test_latest_release_does_not_depend_on_order():
    tags = ["0.1.0", "1.0.0", "0.2.3"]
    assert release_version.latest_release(tags) == (1, 0, 0)
    assert release_version.latest_release(list(reversed(tags))) == (1, 0, 0)


def test_latest_release_strips_whitespace_and_line_endings():
    assert release_version.latest_release(["0.1.0\r", "  0.2.0  ", ""]) == (0, 2, 0)


def test_latest_release_ignores_tags_that_do_not_start_with_a_digit():
    tags = ["1.16.1", "docs-preview", "v9.0.0", "validation-2026", "very-old"]
    assert release_version.latest_release(tags) == (1, 16, 1)


@pytest.mark.parametrize("bad_tag", ["2.0", "2.0.0rc1", "02.0.0", "1.17.0.1", "2026-11-20"])
def test_latest_release_rejects_digit_leading_tag_that_is_not_major_minor_patch(bad_tag):
    # Skipping "2.0" would make the next release 1.17.0, i.e. go backwards.
    with pytest.raises(ValueError):
        release_version.latest_release(PVTLIB_TAGS + [bad_tag])


def test_latest_release_with_prefix_ignores_unprefixed_tags():
    assert release_version.latest_release(["v0.3.0", "1.5.0", "docs"], prefix="v") == (0, 3, 0)


def test_latest_release_with_prefix_rejects_malformed_prefixed_tag():
    with pytest.raises(ValueError):
        release_version.latest_release(["v1.2.5", "v2.0"], prefix="v")


# --- next_version ----------------------------------------------------------------------------------

def test_next_version_from_existing_release():
    assert release_version.next_version((1, 2, 5), "patch") == (1, 2, 6)
    assert release_version.next_version((1, 2, 5), "minor") == (1, 3, 0)
    assert release_version.next_version((1, 2, 5), "major") == (2, 0, 0)


def test_next_version_without_any_release():
    assert release_version.next_version((0, 0, 0), "patch") == (0, 0, 1)
    assert release_version.next_version((0, 0, 0), "minor") == (0, 1, 0)
    assert release_version.next_version((0, 0, 0), "major") == (1, 0, 0)


def test_next_version_carries_past_nine():
    assert release_version.next_version((0, 9, 9), "patch") == (0, 9, 10)
    assert release_version.next_version((0, 9, 9), "minor") == (0, 10, 0)
    assert release_version.next_version((9, 9, 9), "major") == (10, 0, 0)


@pytest.mark.parametrize("bump", ["", "Patch", "MINOR", "build", "pre"])
def test_next_version_rejects_unknown_bump(bump):
    with pytest.raises(ValueError):
        release_version.next_version((1, 2, 5), bump)


# --- format_version --------------------------------------------------------------------------------

def test_format_version():
    assert release_version.format_version((1, 17, 0)) == "1.17.0"
    assert release_version.format_version((0, 1, 0)) == "0.1.0"
    assert release_version.format_version((10, 0, 12)) == "10.0.12"


def test_format_version_round_trips_through_tag():
    for version in [(0, 0, 1), (0, 1, 0), (1, 16, 1), (12, 34, 56)]:
        assert release_version.parse_release_tag(release_version.format_version(version)) == version
        tag = "v" + release_version.format_version(version)
        assert release_version.parse_release_tag(tag, prefix="v") == version


# --- main ------------------------------------------------------------------------------------------

def test_main_first_release(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", _Stdin(""))
    assert release_version.main(["--bump", "minor"]) == 0
    assert capsys.readouterr().out == "0.1.0\n"


def test_main_with_prefix_prints_version_without_prefix(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", _Stdin("v0.1.0\nv0.2.0\n1.5.0\n"))
    assert release_version.main(["--bump", "patch", "--prefix", "v"]) == 0
    assert capsys.readouterr().out == "0.2.1\n"


def test_main_rejects_unknown_bump(monkeypatch):
    monkeypatch.setattr("sys.stdin", _Stdin("1.16.1\n"))
    with pytest.raises(SystemExit):
        release_version.main(["--bump", "build"])


def test_main_requires_bump(monkeypatch):
    monkeypatch.setattr("sys.stdin", _Stdin("1.16.1\n"))
    with pytest.raises(SystemExit):
        release_version.main([])


def test_main_fails_on_malformed_release_tag(monkeypatch):
    monkeypatch.setattr("sys.stdin", _Stdin("1.16.1\n1.17\n"))
    with pytest.raises(ValueError):
        release_version.main(["--bump", "patch"])


class _Stdin:
    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text
