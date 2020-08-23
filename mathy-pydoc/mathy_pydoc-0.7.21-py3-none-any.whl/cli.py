import sys
from typing import Dict, List, Union

import typer

from .document import Document, Index
from .imp import dir_object
from .loader import PythonLoader
from .preprocessor import Preprocessor

app = typer.Typer()


def default_config(config):
    config.setdefault("sort", "name")
    config.setdefault("headers", "markdown")
    config.setdefault("theme", "readthedocs")
    config.setdefault("loader", "mathy_pydoc.loader.PythonLoader")
    config.setdefault("preprocessor", "mathy_pydoc.preprocessor.Preprocessor")
    config.setdefault("additional_search_paths", [])
    return config


def log(*args, **kwargs):
    kwargs.setdefault("file", sys.stderr)
    print(*args, **kwargs)


@app.command()
def main(names: List[str]):
    names = list(names)
    config = default_config({})
    loader = PythonLoader(config)
    preproc = Preprocessor(config)

    # Build the index and document structure first, we load the actual
    # docstrings at a later point.
    log("Building index...")
    index = Index()

    def add_sections(
        doc: Document,
        object_names: Union[List[str], Dict[str, str], str],
        depth: int = 1,
    ):
        if isinstance(object_names, list):
            [add_sections(doc, x, depth) for x in object_names]
        elif isinstance(object_names, dict):
            for key, subsections in object_names.items():
                add_sections(doc, key, depth)
                add_sections(doc, subsections, depth + 1)
        elif isinstance(object_names, str):
            # Check how many levels of recursion we should be going.
            expand_depth = len(object_names)
            object_names = object_names.rstrip("+")
            expand_depth -= len(object_names)

            def create_sections(name, level):
                if level > expand_depth:
                    return
                index.new_section(
                    doc,
                    name,
                    depth=depth + level,
                    header_type=config.get("headers", "html"),
                )
                sort_order = config.get("sort")
                if sort_order not in ("line", "name"):
                    sort_order = "line"
                need_docstrings = "docstring" in config.get("filter", ["docstring"])
                for sub in dir_object(name, sort_order, need_docstrings):
                    sub = name + "." + sub
                    create_sections(sub, level + 1)

            create_sections(object_names, 0)
        else:
            raise RuntimeError(object_names)

    # Make sure that we can find modules from the current working directory,
    # and have them take precedence over installed modules.
    sys.path.insert(0, ".")

    # Generate a single document from the import names specified on the command-line.
    doc = index.new_document("main.md")
    add_sections(doc, names)

    # Load the docstrings and fill the sections.
    log("Started generating documentation...")
    for doc in index.documents.values():
        for section in filter(lambda s: s.identifier, doc.sections):
            loader.load_section(section)
            preproc.preprocess_section(section)

    for section in doc.sections:
        section.render(sys.stdout)
    return 0


if __name__ == "__main__":
    typer.run(main)
