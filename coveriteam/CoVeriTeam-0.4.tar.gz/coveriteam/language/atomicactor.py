# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from benchexec.model import cmdline_for_run, load_tool_info
from benchexec.runexecutor import RunExecutor
import benchexec.containerexecutor as containerexecutor
from benchexec.test_benchmark_definition import DummyConfig
from coveriteam.language.actor import Actor
from coveriteam.language.actorconfig import ActorConfig
from coveriteam.util import (
    TOOL_OUTPUT_FILE,
    str_dict,
    get_additional_paths_for_container_config,
)
import argparse
from pathlib import Path
import os
import uuid
from xml.etree import ElementTree
from coveriteam.language import CoVeriLangException
from benchexec.container import DIR_HIDDEN, DIR_OVERLAY, DIR_READ_ONLY, DIR_FULL_ACCESS
from string import Template


class AtomicActor(Actor):
    def __init__(self, path):
        self.__config = ActorConfig(path)

    def name(self):
        return self.__config.actor_name

    def log_dir(self):
        # actor execution id is for the complete execution of an actor -- atomic or composite
        # atomic execution id is for this specific atomic actor.
        return (
            Actor.get_top_actor_execution_dir()
            / self.name()
            / self._atomic_execution_id
        )

    def log_file(self):
        return self.log_dir() / TOOL_OUTPUT_FILE

    def _get_relative_path_to_tool(self, path):
        return os.path.relpath(path, self.__config.tool_dir) if path else ""

    def print_version(self):
        cwd = os.getcwd()
        os.chdir(self.__config.tool_dir)

        tool_name = self.__config.tool_name or self.name()
        tool_info, self._tool = load_tool_info(tool_name, DummyConfig)
        version = self._tool.version(self._tool.executable())
        print(self._tool.name() + " " + version)
        os.chdir(cwd)

    def act(self, **kwargs):
        # Generate atomic execution id and then call the act method of the super class.
        self._atomic_execution_id = str(uuid.uuid4())
        self.__set_directory_modes(kwargs)
        res = super().act(**kwargs)
        self.gen_xml_elem(kwargs, res)

        return res

    def _act(self, **kwargs):
        args = self._prepare_args(**kwargs)
        d = self._get_arg_substitutions(**kwargs)
        options = [Template(o).safe_substitute(**d) for o in self.__config.options]
        self._run_tool(*args, options)
        try:
            return self._extract_result()
        except UnboundLocalError:
            msg = "The execution of the actor {} did not produce the expected result".format(
                self.name()
            )
            msg += "More information can be found in the logfile produced by the tool: {}".format(
                self.log_file()
            )
            raise CoVeriLangException(msg)

    def _run_tool(self, program_path, property_path, additional_options=[], options=[]):
        # Change directory to tool's directory
        cwd = os.getcwd()
        os.chdir(self.__config.tool_dir)

        program_path = self._get_relative_path_to_tool(program_path)
        property_path = self._get_relative_path_to_tool(property_path)

        tool_name = self.__config.tool_name or self.name()

        tool_info, self._tool = load_tool_info(
            tool_name, self.__create_config_for_container_execution()
        )
        lims_for_exec = {
            "softtimelimit": self.__config.reslim["timelimit"],
            "memlimit": self.__config.reslim["memlimit"],
        }
        cmd = cmdline_for_run(
            self._tool,
            self._tool.executable(),
            options + additional_options,
            [program_path],
            property_path,
            lims_for_exec,
        )

        self.measurements = RunExecutor(dir_modes=self._dir_modes).execute_run(
            cmd,
            str(self.log_file().resolve()),
            output_dir=str(self.log_dir().resolve()),
            result_files_patterns=self._result_files_patterns,
            **lims_for_exec
        )
        # Change back to the original directory
        os.chdir(cwd)

    def gen_xml_elem(self, inputs, outputs):
        super().gen_xml_elem(inputs, outputs)
        data = self.get_measurements_data_for_xml()
        self.xml_elem.append(ElementTree.Element("measurements", str_dict(data)))

    def get_measurements_data_for_xml(self):
        data_filter = ["cputime", "walltime", "memory"]
        data = {k: self.measurements[k] for k in data_filter}
        return str_dict(data)

    def __set_directory_modes(self, inputs):
        # The default directory modes taken from container executor.
        self._dir_modes = {
            "/": DIR_OVERLAY,
            "/run": DIR_HIDDEN,
            "/tmp": DIR_HIDDEN,  # noqa S108
        }
        # Update the default with the /sys as hidden.
        self._dir_modes["/sys"] = DIR_HIDDEN
        self._dir_modes["/sys"] = DIR_HIDDEN
        self._dir_modes[self.__config.tool_dir] = DIR_OVERLAY

        for v in inputs.values():
            if v.path:
                p = str(Path(v.path).parent.resolve())
                self._dir_modes[p] = DIR_OVERLAY

    def __create_config_for_container_execution(self):
        parser = argparse.ArgumentParser()
        containerexecutor.add_basic_container_args(parser)
        containerexecutor.add_container_output_args(parser)
        mp = {
            DIR_HIDDEN: "--hidden-dir",
            DIR_OVERLAY: "--overlay-dir",
            DIR_READ_ONLY: "--read-only-dir",
            DIR_FULL_ACCESS: "--full-access-dir",
        }
        args = []
        for p in get_additional_paths_for_container_config():
            args += ["--full-access-dir", p]
        for k, v in self._dir_modes.items():
            args += [mp[v], k]
        config = parser.parse_args(args)
        config.container = True
        return config

    def _get_arg_substitutions(self, **kwargs):
        return {}
