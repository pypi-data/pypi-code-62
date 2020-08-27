# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import shutil
import sys
import argparse
import coveriteam.util as util
from coveriteam.interpreter.python_code_generator import generate_python_code
import logging
import coveriteam
from coveriteam.language.atomicactor import AtomicActor
from pathlib import Path


class CoVeriTeam:
    def start(self, argv):
        self.config = self.create_argument_parser().parse_args(argv)
        str_to_prepend = ""

        if self.config.clean:
            # Remove both the archive and unzip directory
            shutil.rmtree(util.INSTALL_DIR)
            shutil.rmtree(util.ARCHIVE_DOWNLOAD_PATH)
            shutil.rmtree(util.TOOL_INFO_DOWNLOAD_PATH)

        if self.config.debug:
            FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)

        if self.config.cache_dir:
            util.set_cache_directories(Path(self.config.cache_dir).resolve())
        else:
            util.set_cache_directories()

        if self.config.testtool:
            a = AtomicActor(self.config.input_file)
            a.print_version()
            return

        if self.config.inputs:
            d = dict(self.config.inputs)
            for k in d:
                str_to_prepend += k + " = " + repr(d[k]) + ";\n"

        if self.config.input_file:
            """"CVL file is provided."""
            generated_code = str_to_prepend + generate_python_code(
                self.config.input_file
            )
            if self.config.generate_code:
                print(generated_code)
            else:
                exec(generated_code, globals())  # noqa S102

    def create_argument_parser(self):
        """
        Create a parser for the command-line options.
        @return: an argparse.ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            prog="coveriteam",
            fromfile_prefix_chars="@",
            description="""Execute a program written in CoVeriLang.
               Command-line parameters can additionally be read from a file if file name prefixed with '@' is given as argument.
               """,
        )
        parser.add_argument(
            "--version", action="version", version=f"{coveriteam.__version__}"
        )

        parser.add_argument(
            "--tool-info",
            dest="testtool",
            action="store_true",
            default=False,
            help="Test the given YML file configuration by executing the tool for version.",
        )

        parser.add_argument(
            "input_file",
            metavar="INPUT_FILE",
            help="The program written in CoVeriLang or a YML configuration if testing a tool.",
        )
        parser.add_argument(
            "--input",
            action="append",
            type=lambda kv: kv.split("="),
            dest="inputs",
            help="Inputs to the CoVeriLang program provided in the form of key=val.",
        )

        parser.add_argument(
            "--gen-code",
            dest="generate_code",
            action="store_true",
            default=False,
            help="Flag to generate python code from the cvl file.",
        )

        parser.add_argument(
            "--clean",
            dest="clean",
            action="store_true",
            default=False,
            help="Clean the tmp directory, which contains the extracted archives of the atomic actors.",
        )

        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Set the logging to debug.",
        )

        parser.add_argument(
            "--cache-dir", metavar="CACHE_DIR", help="Path to the cache."
        )
        return parser


def main(argv=None):
    args = argv or sys.argv
    CoVeriTeam().start(args[1:])


if __name__ == "__main__":
    main()
