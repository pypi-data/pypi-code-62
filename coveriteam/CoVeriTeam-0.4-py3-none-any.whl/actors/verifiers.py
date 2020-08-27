# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.language.actor import Verifier
from coveriteam.language.atomicactor import AtomicActor
from coveriteam.language.artifact import (
    CProgram,
    ReachabilityWitness,
    Specification,
    Witness,
    Verdict,
)
import logging


class ProgramVerifier(Verifier, AtomicActor):
    _input_artifacts = {"program": CProgram, "spec": Specification}
    _output_artifacts = {"verdict": Verdict, "witness": Witness}
    _result_files_patterns = ["**/*.graphml"]

    # It is a deliberate decision to not have the init function. We do not want anyone to
    # create instances of this class.

    def _prepare_args(self, program, spec):
        return [program.path, spec.path]

    def _extract_result(self):
        # TODO this could be put in a pattern
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
