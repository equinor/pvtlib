"""Fail if a file tracked by git contains a path from a developer's own machine.

Stored notebook outputs, warnings and tracebacks easily carry paths such as
``C:\\Users\\<name>\\...`` or ``/home/<name>/...`` into the repository. This repository is public,
so such paths must not be committed. The check runs in CI (see ``.github/workflows/tests.yml``)
and can be run locally from the repository root::

    python tools/check_no_local_paths.py

Exit status 0 if no file contains a local path, 1 otherwise. Every hit is printed as
``file:line: text``.

Paths that only exist on CI runners (``/home/runner/...``) are not local paths and are allowed.
"""

import re
import subprocess
import sys
from pathlib import Path

# A Windows drive path ("C:\Users", or "C:\\Users" as written inside JSON and Python strings),
# a Windows user profile folder, or a home folder on Linux/macOS other than the CI runner's.
LOCAL_PATH = re.compile(
    r"\b[A-Za-z]:\\{1,2}[A-Za-z]"
    r"|AppData\\"
    r"|/Users/[A-Za-z0-9._-]+/"
    r"|/home/(?!runner/)[A-Za-z0-9._-]+/"
)
THIS_FILE = Path(__file__).resolve()


def tracked_files():
    """Return the files tracked by git, as paths relative to the repository root.

    Returns
    -------
    list of pathlib.Path
        Tracked files, from ``git ls-files``.
    """
    listing = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True)
    return [Path(name) for name in listing.stdout.decode("utf-8").split("\0") if name]


def local_path_hits(path):
    """Find lines in a file that contain a local path.

    Parameters
    ----------
    path : pathlib.Path
        File to check. Binary files (that are not valid UTF-8) are skipped.

    Returns
    -------
    list of str
        One ``file:line: text`` entry per matching line.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    hits = []
    for number, line in enumerate(text.splitlines(), start=1):
        if LOCAL_PATH.search(line):
            hits.append(f"{path.as_posix()}:{number}: {line.strip()[:200]}")
    return hits


def main():
    hits = []
    for path in tracked_files():
        if path.resolve() == THIS_FILE:
            continue
        hits += local_path_hits(path)
    for hit in hits:
        print(hit)
    if hits:
        print(f"{len(hits)} line(s) contain a local path. Remove them, for example by clearing "
              "the notebook output that holds them.")
        return 1
    print("No local paths found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
