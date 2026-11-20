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

"""Tests that every example is complete and appears on the documentation site.

Each folder in examples/ must have a README.md, and every script and notebook in it must be on the
page generated for it by docs/conf.py. Scripts and notebooks directly in examples/ would not be on
any page, so there must be none.
"""

import importlib.util
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPOSITORY_ROOT / "examples"


def _load_docs_conf():
    spec = importlib.util.spec_from_file_location("pvtlib_docs_conf", REPOSITORY_ROOT / "docs" / "conf.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docs_conf = _load_docs_conf()


def _example_subfolders():
    return sorted(folder for folder in EXAMPLES_DIR.iterdir() if folder.is_dir() and not folder.name.startswith("."))


def test_every_example_folder_has_a_readme():
    missing = [folder.name for folder in _example_subfolders() if not (folder / "README.md").is_file()]
    assert missing == []


def test_every_example_folder_is_on_the_site():
    assert docs_conf._example_folders() == _example_subfolders()


def test_no_script_or_notebook_outside_an_example_folder():
    loose_files = sorted(path.name for path in EXAMPLES_DIR.iterdir() if path.suffix in (".py", ".ipynb"))
    assert loose_files == []


def test_every_script_and_notebook_is_on_its_example_page():
    for folder in _example_subfolders():
        page = docs_conf._example_page(folder)
        page_name = docs_conf._example_page_name(folder)
        for script in folder.glob("*.py"):
            assert f"```{{literalinclude}} ../../examples/{folder.name}/{script.name}\n" in page, script
        for notebook in folder.glob("*.ipynb"):
            assert f"\n{page_name}/{notebook.stem}\n" in page, notebook

