import shutil
import os

from chromie.utils import ChromiePathFinder, ManifestFile
from chromie.enum import Initialize, Path


def make_extension_dir(finder):
    os.mkdir(finder.root)
    os.mkdir(finder(Path.SRC_DIR))
    os.mkdir(finder(Path.IMAGES_DIR))
    os.mkdir(finder(Path.DIST_DIR))
    os.mkdir(finder(Path.STORE_DIR))

    with open(finder(Path.IGNORE_FILE), "w") as f:
        f.write("")

    ManifestFile(
        finder(Path.MANIFEST_FILE),
        {"name": finder.name, "manifest_version": 2, "version": "0.0.0"},
    ).write()


def init(args):

    name = args.name if args.name else input(Initialize.NAME_PROMPT)
    overwrite = args.overwrite

    finder = ChromiePathFinder(args.filepath, name)

    if not overwrite and finder.exists() == True:
        asked = 0
        overwrite_prompt = ""
        while asked <= 3 or overwrite_prompt not in [
            *Initialize.AFFERMATIVE,
            *Initialize.NEGATIVE,
        ]:
            overwrite_prompt = input(Initialize.OVERWRIGHT_PROMPT).upper()
            asked += 1
            if overwrite_prompt in Initialize.NEGATIVE or asked >= 3:
                raise SystemExit()

            elif overwrite_prompt in Initialize.AFFERMATIVE:
                shutil.rmtree(finder.root, ignore_errors=True)
                break

    elif overwrite == True:
        shutil.rmtree(finder.root, ignore_errors=True)

    if not finder.exists(finder.root):
        make_extension_dir(finder)
