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

"""Work out the version of the next release from the existing git tags.

Used by the release workflow, ``.github/workflows/release.yml``. pvtlib releases are tagged
``MAJOR.MINOR.PATCH`` without a prefix (for example ``1.16.1``), and the next version is the
latest release with one part increased:

========  ===========  ===============
bump      from 1.16.1  from no release
========  ===========  ===============
patch     1.16.2       0.0.1
minor     1.17.0       0.1.0
major     2.0.0        1.0.0
========  ===========  ===============

Usage, with the tags on standard input, one per line::

    git tag --list | python tools/release_version.py --bump minor

prints the version, for example ``1.17.0``. ``--prefix`` sets the text release tags start with;
it is empty for pvtlib, ``--prefix v`` would read tags like ``v1.2.5``. The printed version never
has the prefix.

Tags that do not start with the prefix followed by a digit are not release tags and are ignored. A
tag that does, but is not exactly ``<prefix>MAJOR.MINOR.PATCH``, is an error rather than being
skipped: it was most likely meant as a release, and skipping it could make the next release go
backwards.
"""

import argparse
import re
import sys

VERSION_PATTERN = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
BUMPS = ("patch", "minor", "major")


def parse_release_tag(tag: str, prefix: str = "") -> tuple[int, int, int]:
    """Read the version from a release tag.

    Parameters
    ----------
    tag : str
        A release tag, ``<prefix>MAJOR.MINOR.PATCH`` with no leading zeros, for example
        ``"1.16.1"`` with the empty prefix.
    prefix : str
        Text every release tag starts with. Empty for pvtlib.

    Returns
    -------
    tuple of int
        ``(major, minor, patch)``.

    Raises
    ------
    ValueError
        If ``tag`` is not exactly ``<prefix>MAJOR.MINOR.PATCH``.
    """
    match = re.fullmatch(re.escape(prefix) + VERSION_PATTERN, tag)
    if match is None:
        raise ValueError(f"{tag!r} is not a release tag of the form {prefix}MAJOR.MINOR.PATCH, "
                         f"e.g. {prefix}1.2.5")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def latest_release(tags: list[str], prefix: str = "") -> tuple[int, int, int]:
    """Find the highest released version among a list of git tags.

    Parameters
    ----------
    tags : list of str
        Git tag names. Blank entries and surrounding whitespace are ignored. Tags that do not start
        with ``prefix`` followed by a digit are not release tags and are skipped.
    prefix : str
        Text every release tag starts with. Empty for pvtlib.

    Returns
    -------
    tuple of int
        ``(major, minor, patch)`` of the highest release, compared numerically (``1.10.0`` is
        higher than ``1.9.0``), or ``(0, 0, 0)`` if there are no release tags.

    Raises
    ------
    ValueError
        If a tag starts with ``prefix`` and a digit but is not exactly
        ``<prefix>MAJOR.MINOR.PATCH``.
    """
    looks_like_release_tag = re.compile(re.escape(prefix) + "[0-9]")
    versions = [(0, 0, 0)]
    for tag in tags:
        tag = tag.strip()
        if looks_like_release_tag.match(tag):
            versions.append(parse_release_tag(tag, prefix))
    return max(versions)


def next_version(current: tuple[int, int, int], bump: str) -> tuple[int, int, int]:
    """Increase one part of a version, following semantic versioning.

    Parameters
    ----------
    current : tuple of int
        ``(major, minor, patch)`` of the latest release; ``(0, 0, 0)`` if there is none.
    bump : str
        ``"patch"``, ``"minor"`` or ``"major"``. The parts after the one increased are reset to 0.

    Returns
    -------
    tuple of int
        ``(major, minor, patch)`` of the next release.

    Raises
    ------
    ValueError
        If ``bump`` is not one of the three names.
    """
    major, minor, patch = current
    if bump == "patch":
        return major, minor, patch + 1
    if bump == "minor":
        return major, minor + 1, 0
    if bump == "major":
        return major + 1, 0, 0
    raise ValueError(f"bump must be one of {BUMPS}, got {bump!r}")


def format_version(version: tuple[int, int, int]) -> str:
    """Write a version as text without the tag prefix, for example ``"1.17.0"``."""
    return ".".join(str(part) for part in version)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Work out the version of the next release from the git tags.")
    parser.add_argument("--bump", required=True, choices=BUMPS)
    parser.add_argument("--prefix", default="", help="text release tags start with (default: none)")
    args = parser.parse_args(argv)

    tags = sys.stdin.read().splitlines()
    print(format_version(next_version(latest_release(tags, args.prefix), args.bump)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
