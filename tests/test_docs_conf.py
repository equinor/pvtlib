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

"""Tests for the helper functions in the Sphinx configuration, docs/conf.py: the generated example
pages, the rewriting of Markdown links and the plain-text footnotes in docstrings."""

import importlib.util
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/equinor/pvtlib"
README = REPOSITORY_ROOT / "README.md"
EXAMPLES_README = REPOSITORY_ROOT / "examples" / "README.md"


def _load_docs_conf():
    spec = importlib.util.spec_from_file_location("pvtlib_docs_conf", REPOSITORY_ROOT / "docs" / "conf.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


docs_conf = _load_docs_conf()


# --- Example pages ---------------------------------------------------------------------------------

def test_example_page_name():
    assert docs_conf._example_page_name(Path("01 Gas Properties from AGA8")) == "01-gas-properties-from-aga8"
    assert docs_conf._example_page_name(Path("14 Lockhart-Martinelli and Froude Numbers")) == \
        "14-lockhart-martinelli-and-froude-numbers"
    assert docs_conf._example_page_name(Path("single")) == "single"


def test_example_page_with_scripts_and_notebooks(tmp_path):
    folder = tmp_path / "20 New Example"
    folder.mkdir()
    (folder / "README.md").write_text("# 20 New Example\n", encoding="utf-8")
    (folder / "b_second.py").write_text("", encoding="utf-8")
    (folder / "a_first.py").write_text("", encoding="utf-8")
    (folder / "notebook.ipynb").write_text("{}", encoding="utf-8")
    (folder / "data.csv").write_text("", encoding="utf-8")

    expected = "\n".join([
        "```{include} ../../examples/20 New Example/README.md",
        ":relative-images:",
        "```",
        "",
        "## Source code",
        "",
        "```{literalinclude} ../../examples/20 New Example/a_first.py",
        ":caption: a_first.py",
        ":language: python",
        "```",
        "",
        "```{literalinclude} ../../examples/20 New Example/b_second.py",
        ":caption: b_second.py",
        ":language: python",
        "```",
        "",
        "## Notebooks",
        "",
        "```{toctree}",
        ":maxdepth: 1",
        "",
        "20-new-example/notebook",
        "```",
        "",
    ])
    assert docs_conf._example_page(folder) == expected


def test_example_page_with_readme_only(tmp_path):
    folder = tmp_path / "21 Readme Only"
    folder.mkdir()
    (folder / "README.md").write_text("# 21\n", encoding="utf-8")
    expected = "```{include} ../../examples/21 Readme Only/README.md\n:relative-images:\n```\n"
    assert docs_conf._example_page(folder) == expected


def test_examples_index_page_lists_pages_in_given_order():
    folders = [Path("01 Gas Properties from AGA8"), Path("10 Gas Mixing Calculation")]
    expected = "\n".join([
        "```{include} ../../examples/README.md",
        "```",
        "",
        "```{toctree}",
        ":hidden:",
        "",
        "01-gas-properties-from-aga8",
        "10-gas-mixing-calculation",
        "```",
        "",
    ])
    assert docs_conf._examples_index_page(folders) == expected


def test_write_example_pages_copies_notebooks_and_removes_stale_files(tmp_path, monkeypatch):
    examples_dir = tmp_path / "examples"
    first = examples_dir / "01 First"
    second = examples_dir / "02 Second"
    for folder in [first, second]:
        folder.mkdir(parents=True)
        (folder / "README.md").write_text(f"# {folder.name}\n", encoding="utf-8")
    (second / "calc.ipynb").write_text('{"cells": []}', encoding="utf-8")
    (examples_dir / "no readme").mkdir()
    pages_dir = tmp_path / "_examples"
    (pages_dir / "03-removed").mkdir(parents=True)
    (pages_dir / "03-removed" / "old.ipynb").write_text("{}", encoding="utf-8")
    (pages_dir / "03-removed.md").write_text("old", encoding="utf-8")
    (pages_dir / "02-second").mkdir()
    (pages_dir / "02-second" / "renamed.ipynb").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(docs_conf, "EXAMPLES_DIR", examples_dir)
    monkeypatch.setattr(docs_conf, "EXAMPLE_PAGES_DIR", pages_dir)

    docs_conf._write_example_pages(app=None)

    assert sorted(path.relative_to(pages_dir).as_posix() for path in pages_dir.rglob("*")) == [
        "01-first.md", "02-second", "02-second.md", "02-second/calc.ipynb", "index.md"]
    assert (pages_dir / "02-second" / "calc.ipynb").read_text(encoding="utf-8") == '{"cells": []}'
    assert (pages_dir / "02-second.md").read_text(encoding="utf-8") == docs_conf._example_page(second)
    assert (pages_dir / "index.md").read_text(encoding="utf-8") == docs_conf._examples_index_page([first, second])


# --- Links from Markdown ---------------------------------------------------------------------------

def test_link_to_repository_file_points_at_github():
    text = "see the [LICENSE](LICENSE) file"
    expected = f"see the [LICENSE]({REPOSITORY_URL}/tree/main/LICENSE) file"
    assert docs_conf._link_repository_files(text, README) == expected


def test_link_to_examples_folder_points_at_examples_page():
    text = "[examples](examples)"
    assert docs_conf._link_repository_files(text, README) == "[examples](project:/_examples/index.md)"


def test_link_to_example_folder_and_its_readme_point_at_its_page():
    text = "[a](examples/12%20Coriolis%20Pressure%20Correction) [b](examples/13%20Ultrasonic%20Wetgas%20Van%20Putten/README.md)"
    expected = ("[a](project:/_examples/12-coriolis-pressure-correction.md) "
                "[b](project:/_examples/13-ultrasonic-wetgas-van-putten.md)")
    assert docs_conf._link_repository_files(text, README) == expected


def test_link_to_notebook_points_at_rendered_notebook():
    text = "[notebook](10%20Gas%20Mixing%20Calculation/gas_mixing_calculation.ipynb)"
    expected = "[notebook](project:/_examples/10-gas-mixing-calculation/gas_mixing_calculation.ipynb)"
    assert docs_conf._link_repository_files(text, EXAMPLES_README) == expected


def test_link_to_example_script_points_at_github():
    text = "[script](01%20Gas%20Properties%20from%20AGA8/gas_properties_from_aga8.py)"
    expected = (f"[script]({REPOSITORY_URL}/tree/main/examples/"
                "01%20Gas%20Properties%20from%20AGA8/gas_properties_from_aga8.py)")
    assert docs_conf._link_repository_files(text, EXAMPLES_README) == expected


def test_link_to_documentation_page_is_unchanged():
    text = "[releasing](docs/releasing.md)"
    assert docs_conf._link_repository_files(text, README) == text


def test_image_link_is_unchanged():
    example_readme = REPOSITORY_ROOT / "examples" / "14 Lockhart-Martinelli and Froude Numbers" / "README.md"
    text = "![surface](lockhart_martinelli_surface.png)"
    assert docs_conf._link_repository_files(text, example_readme) == text


def test_external_anchor_missing_and_outside_links_are_unchanged():
    text = ("[pypi](https://pypi.org/project/pvtlib/) [section](#usage) [missing](no_such_file.txt) "
            "[parent](..) [page](project:/api.rst)")
    assert docs_conf._link_repository_files(text, README) == text


# --- Footnotes in docstrings -----------------------------------------------------------------------

def test_footnote_references_and_definitions_become_text():
    lines = [
        "Calculated according to ISO 5167-4:2022 [1]_ and [2_].",
        "",
        ".. rubric:: References",
        "",
        ".. [1] ISO 5167-4:2022",
        ".. [2] A paper whose title",
        "   continues on the next line",
        "",
        "Text after the references [1]_.",
    ]
    expected = [
        "Calculated according to ISO 5167-4:2022 [1] and [2].",
        "",
        ".. rubric:: References",
        "",
        "",
        "- [1] ISO 5167-4:2022",
        "",
        "- [2] A paper whose title",
        "  continues on the next line",
        "",
        "Text after the references [1].",
    ]
    assert docs_conf._footnotes_as_text(lines) == expected


def test_indented_footnote_definition_keeps_its_indent():
    lines = ["    .. [1] Reference", "        continued", "    Next paragraph"]
    expected = ["", "    - [1] Reference", "      continued", "    Next paragraph"]
    assert docs_conf._footnotes_as_text(lines) == expected


def test_lines_without_footnotes_are_unchanged():
    lines = ["Pressure [bara] and list item [a]", "", "x = y[1]"]
    assert docs_conf._footnotes_as_text(lines) == lines
