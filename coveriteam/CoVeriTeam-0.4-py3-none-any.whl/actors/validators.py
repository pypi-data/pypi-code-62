# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.language.artifact import (
    CProgram,
    ReachabilityWitness,
    Verdict,
    Witness,
    Specification,
)
from coveriteam.language.actor import Validator
from coveriteam.language.atomicactor import AtomicActor
import logging


class ProgramValidator(Validator, AtomicActor):
    _input_artifacts = {
        "program": CProgram,
        "spec": Specification,
        "witness": Witness,
        "verdict": Verdict,
    }
    _output_artifacts = {"verdict": Verdict, "witness": Witness}
    _result_files_patterns = ["**/*.graphml"]

    def _get_arg_substitutions(self, program, spec, witness, verdict):
        return {"witness": self._get_relative_path_to_tool(witness.path)}

    def _prepare_args(self, program, spec, witness, verdict):
        return [program.path, spec.path]

    def _extract_result(self):
        # read output
        try:
            with open(self.log_file(), "rt", errors="ignore") as outputFile:
                output = outputFile.readlines()
                # first 6 lines are for logging, rest is output of subprocess, see runexecutor.py for details
                output = output[6:]
        except IOError as e:
            logging.warning("Cannot read log file: %s", e.strerror)
            output = []

        verdict = Verdict(self._tool.determine_result(0, 0, output, False))

        # extract result
        for file in self.log_dir().glob("**/*.graphml"):
            witness = ReachabilityWitness(file)

        return {"verdict": verdict, "witness": witness}
