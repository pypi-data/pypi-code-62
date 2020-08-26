from argparse import ArgumentParser, FileType
from os import system
from os.path import dirname, realpath
from shutil import copytree, rmtree
from urllib.request import urlopen

from .parser import ApiParser
from .generators.python import PythonApiGenerator


def main():
    # get the arguments
    parser = ArgumentParser(
        prog="telegen", description="A CLI tool that generates code by parsing the Telegram Bot API page"
    )
    parser.add_argument("language", help="Output language")
    parser.add_argument(
        "src",
        help="Source file (will be fetched if not passed)",
        nargs="?",
        type=FileType("r"),
        default=None,
    )
    parser.add_argument(
        "--overwrite", "-o", help="Delete conflicting files before emitting (default: exit)", action="store_true"
    )
    args = parser.parse_args()

    # variables
    module_dir = dirname(realpath(__file__))
    language = args.language
    output_dir = f"telegen_{language}"

    # delete the output directory if the flag is set and prepare a new one
    if args.overwrite:
        rmtree(output_dir, ignore_errors=True)

    copytree(f"{module_dir}/includes/{language}", output_dir)

    # get the source from the given file or fetch it from the URL
    src = args.src or urlopen("https://core.telegram.org/bots/api")

    # generate the code
    parser = ApiParser()
    api_version, endpoints, types, reversed_aliases = parser.parse(src)

    languages = {"python": PythonApiGenerator}

    generator = languages[language]()
    generated = generator.generate(api_version, endpoints, types, reversed_aliases)

    # write the files
    for filename, content in generated:
        with open(f"{output_dir}/{filename}", "w+") as f:
            f.write(content)
