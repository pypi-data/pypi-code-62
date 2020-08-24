import sys
from os import listdir
from os.path import isdir, join
from subprocess import call

import click


@click.command()
@click.argument("langs", nargs=-1)
def download(langs):
    """
    LANGS Programming languages to download
    """
    from tree_sitter import Language

    for lang in langs:
        out = f"../grammars/tree-sitter-{lang}"
        try:
            clone_url = f"https://github.com/tree-sitter/tree-sitter-{lang}"
            call(["git", "clone", "--depth", "1", clone_url, out])
        except:
            continue

    out = f"../grammars/"
    languages = [join(out, f) for f in listdir(out) if isdir(join(out, f))]
    Language.build_library(join(out, "languages.so"), languages)

    return 0


if __name__ == '__main__':
    sys.exit(download())
