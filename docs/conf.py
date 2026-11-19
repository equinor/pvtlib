# Sphinx configuration for the pvtlib documentation site (https://equinor.github.io/pvtlib/).
#
# The site is assembled from files the repository keeps anyway:
# - README.md is the start page and docs/*.md hold the remaining pages,
# - every folder in examples/ gets a page with its README, its scripts and its notebooks,
# - the API reference is generated from the NumPy-style docstrings in pvtlib.
#
# Build locally with:
#     pip install -e .[docs]
#     sphinx-build -W --keep-going -b html docs docs/_build/html

from __future__ import annotations

import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote

import pvtlib

DOCS_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = DOCS_DIR.parent
REPOSITORY_URL = "https://github.com/equinor/pvtlib"

project = "pvtlib"
author = "Christian Hågenvik"
copyright = "2025, Christian Hågenvik"
release = pvtlib.__version__
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "myst_nb",
]

exclude_patterns = ["_build", "**.ipynb_checkpoints"]

# Suffixes of the documentation pages in docs/. Links in Markdown to these files are left to Sphinx.
DOCUMENTATION_SUFFIXES = {".md", ".rst", ".ipynb"}

# --- API reference from the docstrings -----------------------------------------------------------
# autosummary generates one page per module of pvtlib (recursively), including modules added later.
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": True,
}
autodoc_typehints = "description"
autodoc_class_signature = "separated"

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_rtype = False
napoleon_use_ivar = True

# The AGA8 class documents its methods in a "Methods" section. It is rendered like a parameter list;
# napoleon's default would declare the methods a second time next to autodoc's own entries.
napoleon_custom_sections = [("Methods", "params_style")]

# The docstrings cite their references as numbered footnotes, [1]_ and .. [1], as is usual in
# NumPy-style docstrings. autosummary puts all functions of a module on one page, where the same
# footnote number occurs many times and docutils cannot tell the footnotes apart, and the summary
# tables would contain references without a target. On the site the references are therefore shown
# as plain text, "[1]" in the text and a list "[1] <reference>" under References, exactly as they
# read in help(). The docstrings themselves are not changed.
# Several docstrings write the reference as [1_] instead of [1]_; both are shown as [1].
_FOOTNOTE_REFERENCE = re.compile(r"\[(\d+)(?:\]_|_\])")
_FOOTNOTE_DEFINITION = re.compile(r"^(?P<indent>\s*)\.\.\s+\[(?P<number>\d+)\]\s*(?P<text>.*)$")


def _footnotes_as_text(lines):
    """Replace numbered footnotes in docstring lines with plain text.

    Parameters
    ----------
    lines : list of str
        Docstring lines as passed by autodoc.

    Returns
    -------
    list of str
        The lines with each reference ``[1]_`` (or ``[1_]``) replaced by ``[1]``, and each footnote definition
        ``.. [1] text`` replaced by a list item ``- [1] text`` preceded by a blank line. Indented
        continuation lines of a definition are re-indented to belong to the list item.
    """
    rewritten = []
    definition_indent = None
    for line in lines:
        definition = _FOOTNOTE_DEFINITION.match(line)
        if definition:
            definition_indent = definition["indent"]
            rewritten += ["", f"{definition_indent}- [{definition['number']}] {definition['text']}".rstrip()]
            continue
        line_indent = len(line) - len(line.lstrip())
        if definition_indent is not None and line.strip():
            if line_indent > len(definition_indent):
                rewritten.append(f"{definition_indent}  {line.strip()}")
                continue
            definition_indent = None
        rewritten.append(_FOOTNOTE_REFERENCE.sub(r"[\1]", line))
    return rewritten


def _on_autodoc_process_docstring(app, what, name, obj, options, lines):
    lines[:] = _footnotes_as_text(lines)


# --- Markdown and notebooks ----------------------------------------------------------------------
# dollarmath renders the $ ... $ and $$ ... $$ equations the same way GitHub does.
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
]
myst_heading_anchors = 3
# The notebooks are shown with the outputs stored in them. They are not executed when the site is
# built; the "examples" job in .github/workflows/tests.yml runs them.
nb_execution_mode = "off"

# --- HTML -----------------------------------------------------------------------------------------
html_theme = "furo"
html_title = f"{project} {release}"


# --- Example pages --------------------------------------------------------------------------------
# The example pages are generated in docs/_examples/ (ignored by git) when a build starts. A page
# shows the README of the example folder, the source code of its scripts and links to its notebooks,
# which are copied next to the page and rendered by MyST-NB. Adding an example folder therefore needs
# no change in docs/. tests/test_examples.py checks that every folder has a README and that every
# script and notebook is on a page.
EXAMPLES_DIR = REPOSITORY_ROOT / "examples"
EXAMPLE_PAGES_DIR = DOCS_DIR / "_examples"


def _example_folders():
    """Example folders, in name order: the subfolders of examples/ that contain a README.md.

    Returns
    -------
    list of pathlib.Path
        Absolute paths of the example folders.
    """
    return sorted(folder for folder in EXAMPLES_DIR.iterdir()
                  if folder.is_dir() and (folder / "README.md").is_file())


def _example_page_name(example_folder):
    """Page name of an example folder, e.g. '01 Gas Properties from AGA8' -> '01-gas-properties-from-aga8'.

    Parameters
    ----------
    example_folder : pathlib.Path
        Path of the example folder.

    Returns
    -------
    str
        Lower-case folder name with spaces replaced by hyphens.
    """
    return example_folder.name.lower().replace(" ", "-")


def _example_page(example_folder):
    """Markdown source of the page for one example: its README, the source of each script and a
    table of contents with the rendered notebooks.

    Parameters
    ----------
    example_folder : pathlib.Path
        Absolute path of the example folder.

    Returns
    -------
    str
        Markdown for a page in docs/_examples/; the paths in it are relative to that folder. The
        notebooks are expected as copies in docs/_examples/<page name>/ (see
        :func:`_write_example_pages`).
    """
    relative_folder = "../../examples/" + example_folder.name
    lines = [f"```{{include}} {relative_folder}/README.md", ":relative-images:", "```", ""]
    scripts = sorted(example_folder.glob("*.py"))
    if scripts:
        lines += ["## Source code", ""]
    for script in scripts:
        lines += [f"```{{literalinclude}} {relative_folder}/{script.name}",
                  f":caption: {script.name}",
                  ":language: python",
                  "```",
                  ""]
    notebooks = sorted(example_folder.glob("*.ipynb"))
    if notebooks:
        lines += ["## Notebooks", "", "```{toctree}", ":maxdepth: 1", ""]
        lines += [f"{_example_page_name(example_folder)}/{notebook.stem}" for notebook in notebooks]
        lines += ["```", ""]
    return "\n".join(lines)


def _examples_index_page(example_folders):
    """Markdown source of the examples overview page: examples/README.md and a table of contents.

    Parameters
    ----------
    example_folders : list of pathlib.Path
        Example folders to list, in the order they should appear.

    Returns
    -------
    str
        Markdown for docs/_examples/index.md.
    """
    lines = ["```{include} ../../examples/README.md", "```", "", "```{toctree}", ":hidden:", ""]
    lines += [_example_page_name(folder) for folder in example_folders]
    lines += ["```", ""]
    return "\n".join(lines)


def _write_if_changed(path, content):
    if not path.exists() or path.read_bytes() != content:
        path.write_bytes(content)


def _write_example_pages(app):
    """Write docs/_examples/ from examples/: one page per example folder, a copy of each notebook
    in a subfolder named after the page, and the overview page. Files are only rewritten when their
    content changes, and pages, folders and notebooks of examples that no longer exist are removed.
    """
    example_folders = _example_folders()
    pages = {"index.md": _examples_index_page(example_folders)}
    notebooks = {}
    for folder in example_folders:
        page_name = _example_page_name(folder)
        pages[page_name + ".md"] = _example_page(folder)
        notebooks[page_name] = sorted(folder.glob("*.ipynb"))

    EXAMPLE_PAGES_DIR.mkdir(exist_ok=True)
    for old_entry in EXAMPLE_PAGES_DIR.iterdir():
        if old_entry.is_file() and old_entry.name not in pages:
            old_entry.unlink()
        elif old_entry.is_dir() and not notebooks.get(old_entry.name):
            shutil.rmtree(old_entry)
    for name, content in pages.items():
        _write_if_changed(EXAMPLE_PAGES_DIR / name, content.encode("utf-8"))
    for page_name, page_notebooks in notebooks.items():
        if not page_notebooks:
            continue
        notebook_dir = EXAMPLE_PAGES_DIR / page_name
        notebook_dir.mkdir(exist_ok=True)
        names = {notebook.name for notebook in page_notebooks}
        for old_copy in notebook_dir.iterdir():
            if old_copy.name not in names:
                old_copy.unlink()
        for notebook in page_notebooks:
            _write_if_changed(notebook_dir / notebook.name, notebook.read_bytes())


# --- Relative links in Markdown --------------------------------------------------------------------
# README.md and the example READMEs are written for GitHub and use relative links to files in the
# repository. On the site, a link to an example folder, its README or one of its notebooks goes to
# the generated page instead, and a link to any other repository file goes to that file on GitHub.
_MARKDOWN_LINK = re.compile(r"\]\((?P<target>[^)\s]+)\)")


def _link_repository_files(markdown_text, markdown_file):
    """Point relative Markdown links to the examples at their pages, and to other
    non-documentation repository files at GitHub.

    Parameters
    ----------
    markdown_text : str
        Markdown source.
    markdown_file : pathlib.Path
        Absolute path of the file the text was read from; relative links resolve against it.

    Returns
    -------
    str
        The text with links to examples/, to an example folder or its README.md, and to a notebook
        in an example folder replaced by ``project:/_examples/...`` links (MyST resolves those from
        the documentation root, whichever page the text ends up in), and links to other existing
        repository files that are not documentation pages replaced by absolute GitHub URLs. Images,
        links to documentation pages, external URLs, anchors and paths that do not exist are
        returned unchanged.
    """
    example_folders = _example_folders()

    def replace(match):
        target = match["target"]
        if "://" in target or target.startswith(("#", "mailto:", "project:")):
            return match[0]
        path_part = unquote(target.split("#", 1)[0])
        resolved = (markdown_file.parent / path_part).resolve()
        if not resolved.exists() or not resolved.is_relative_to(REPOSITORY_ROOT):
            return match[0]
        prefix = markdown_text[:match.start()]
        is_image = prefix.rfind("![") > prefix.rfind("]")
        if is_image:
            return match[0]
        if resolved.is_relative_to(DOCS_DIR) and resolved.suffix in DOCUMENTATION_SUFFIXES:
            return match[0]
        if resolved == EXAMPLES_DIR:
            return "](project:/_examples/index.md)"
        if resolved in example_folders:
            return f"](project:/_examples/{_example_page_name(resolved)}.md)"
        if resolved.parent in example_folders and resolved.name == "README.md":
            return f"](project:/_examples/{_example_page_name(resolved.parent)}.md)"
        if resolved.parent in example_folders and resolved.suffix == ".ipynb":
            return f"](project:/_examples/{_example_page_name(resolved.parent)}/{resolved.name})"
        relative = resolved.relative_to(REPOSITORY_ROOT).as_posix()
        return f"]({REPOSITORY_URL}/tree/main/{quote(relative)})"

    return _MARKDOWN_LINK.sub(replace, markdown_text)


def _on_include_read(app, relative_path, parent_docname, content):
    included_file = (Path(app.srcdir) / relative_path).resolve()
    if included_file.suffix == ".md":
        content[0] = _link_repository_files(content[0], included_file)


def _on_source_read(app, docname, source):
    source_file = Path(app.env.doc2path(docname)).resolve()
    if source_file.suffix == ".md":
        source[0] = _link_repository_files(source[0], source_file)


def setup(app):
    app.connect("builder-inited", _write_example_pages)
    app.connect("autodoc-process-docstring", _on_autodoc_process_docstring)
    app.connect("include-read", _on_include_read)
    app.connect("source-read", _on_source_read)
