# Releasing pvtlib

Each release is a git tag `MAJOR.MINOR.PATCH` without a prefix, for example `1.17.0`, the same
files on [PyPI](https://pypi.org/project/pvtlib/), and a GitHub release that lists the changes and
carries those files. Releases are made by the workflow
[`release.yml`](../.github/workflows/release.yml), started by hand. Nothing is released by merging
or pushing.

## Version numbers

Versions follow [semantic versioning](https://semver.org/):

| Part | Increase when | Example |
|---|---|---|
| PATCH | a fix that does not change the documented behaviour or any calculated result | 1.16.1 → 1.16.2 |
| MINOR | new functionality that existing code keeps working with | 1.16.1 → 1.17.0 |
| MAJOR | a change that breaks existing code or the documented behaviour | 1.16.1 → 2.0.0 |

Project rule: a change to calculated results - a new or corrected correlation, constant, unit
handling or reference data - is at least MINOR, even when it is a correction, so it never arrives
unnoticed in a patch update. Dropping support for a Python version is also at least MINOR. Describe
the effect on results in the pull request; the release notes are generated from the pull request
titles.

The version is not written anywhere in the code or in `pyproject.toml`.
[setuptools-scm](https://setuptools-scm.readthedocs.io/) reads it from the git tags when the
package is built or installed, and writes it to `pvtlib/_version.py` (not committed).
`pvtlib.__version__` reports it:

| Installed from | `pvtlib.__version__` |
|---|---|
| PyPI, or the tag `1.17.0` | `1.17.0` |
| a commit after `1.17.0` | a development version such as `1.17.1.dev3+g1a2b3c4` |
| a source tree that was never installed | `0+unknown` |

Building or installing from a git checkout needs the tags: a shallow clone without them gets a
version such as `0.1.dev1+g1a2b3c4`. An editable install (`pip install -e .`) records the version
when it is installed; after pulling new commits or tags, run `pip install -e .` again.
`tests/test_version.py` fails while the installed metadata and `pvtlib.__version__` differ.

## Making a release

1. Merge what should be in the release into `main`, with the checks green.
2. On GitHub, open **Actions → Release → Run workflow**, keep the branch `main`, and choose which
   part of the version to increase (`patch`, `minor` or `major`). The new version is the highest
   existing `MAJOR.MINOR.PATCH` tag with that part increased.
3. The workflow runs on the commit `main` pointed at when it was started:
   1. **prepare** - stops unless the run is on `main`; works out the version
      ([`tools/release_version.py`](../tools/release_version.py)) and stops if that tag already
      exists or PyPI already has that version.
   2. **test** - the complete test workflow, [`tests.yml`](../.github/workflows/tests.yml).
   3. **build** - tags the commit locally (the tag is not pushed), builds the sdist and the wheel
      once, checks that both carry the new version and pass `twine check --strict`, installs each
      in a clean virtual environment and runs the test suite against the installed package (from a
      copy of `tests/` outside the checkout, with a check inside the pytest session that `pvtlib`
      is imported from that environment). Exactly those files are kept, with their SHA-256 in a
      manifest.
   4. **publish** - waits for approval in the environment `pypi` (the only approval in the run).
      It checks the files against the manifest and what PyPI already has, creates the tag at the
      tested commit, uploads the files to PyPI with
      [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (no token; PyPI also stores
      a signed attestation of where each file was built), and then checks that PyPI holds exactly
      those files with the same SHA-256.
   5. **github-release** - creates the GitHub release for the tag, with notes generated from the
      merged pull requests and the same files attached.
4. Edit the release notes on GitHub if the effect on calculated results needs explaining.

Nothing is rebuilt between testing and publishing. If anything fails before the `publish` job, or
in it before the tag is created, nothing is published and a new run can simply be started.

## When a release run fails

- Use **Re-run failed jobs** in the same run. Do not use *Re-run all jobs*; the `prepare` job
  refuses to run in a later attempt, because it would work out a different version.
- A re-run accepts a tag or PyPI files left by an earlier attempt of the same run only if they match
  exactly: the tag must point at the same commit, and every file already on PyPI must have the
  SHA-256 in the manifest and an attestation from this repository's `release.yml` in the
  environment `pypi`. Missing files are then uploaded; existing GitHub release assets must match
  the manifest.
- Never start a new run for a version that already has files on PyPI. PyPI never accepts a file
  name twice, even after it is deleted, so a mistake in a published version is corrected with a
  new version.
- Never move or delete a published tag.
- The artifacts of a run are kept for 90 days, so a failed run must be completed within that time.

## One-time repository setup

These are settings made once by a repository administrator.

- **Environment** - *Settings → Environments*: create `pypi`, add *Required reviewers*, and under
  *Deployment branches and tags* choose *Selected branches and tags* with only `main`. Without
  reviewers, the workflow does not wait for approval before tagging and publishing.
- **Trusted publisher** - on pypi.org, *pvtlib → Manage → Publishing*: add a GitHub trusted
  publisher with owner `equinor`, repository `pvtlib`, workflow `release.yml` and environment
  `pypi`. No PyPI token is stored in the repository.
- **Protect release tags** (optional) - *Settings → Rules → Rulesets → New tag ruleset*, target
  `refs/tags/[0-9]*`, with *Restrict updates* and *Restrict deletions*, so a published tag cannot
  be moved or removed. Do not enable *Restrict creations* unless the workflow is allowed to bypass
  it, as the workflow creates the tag.

## Python versions

pvtlib supports the Python versions listed in `requires-python` and the classifiers in
`pyproject.toml`. The test workflow runs on all of them. When a Python version is dropped, pip on
that Python keeps installing the last release that supported it.
