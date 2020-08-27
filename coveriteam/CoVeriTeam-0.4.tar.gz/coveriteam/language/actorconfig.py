# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import sys
import yaml
from zipfile import ZipFile
import benchexec
from pathlib import Path
from coveriteam.util import (
    make_url,
    is_url,
    download,
    unzip,
    create_cache_directories,
)
import coveriteam.util as util


class ActorDefinitionLoader(yaml.SafeLoader):
    def __init__(self, stream):

        self._root = Path(stream.name).parent
        super(ActorDefinitionLoader, self).__init__(stream)

    def include(self, node):

        filename = self._root / self.construct_scalar(node)
        with filename.open("r") as f:
            return yaml.load(f, ActorDefinitionLoader)  # noqa S506


class ActorConfig:
    def __init__(self, path):
        ActorDefinitionLoader.add_constructor("!include", ActorDefinitionLoader.include)
        create_cache_directories()
        self.path = path
        self.get_actor_config()
        self.actor_name = self._config["actor_name"]
        self.archive_location = self._config["archive"]["location"]
        self.options = self._config["options"]
        self.reslim = self._config["resourcelimits"]
        # Keeping this path as str instead of Path because it is going to be used with string paths mostly.
        self.tool_dir = str(self.__install_if_needed())
        self.__resolve_tool_info_module()

    def get_actor_config(self):
        self._config = self.__yaml_to_dict()
        self._config = ActorConfig.resolve_yaml_file_inclusion(self._config)
        self.__check_actor_definition_integrity()
        self.__sanitize_yaml_dict()

    def __yaml_to_dict(self):
        with open(self.path, "r") as f:
            try:
                d = yaml.load(f, ActorDefinitionLoader)  # noqa S506
            except yaml.YAMLError as e:
                sys.exit(
                    "Actor config yaml file {} is invalid: {}".format(self.path, e)
                )

            return d

    @staticmethod
    def resolve_yaml_file_inclusion(d):
        # Check if "imports" exist
        imports = d.pop("imports", None)
        if not imports:
            return d

        if isinstance(imports, list):
            di = {}
            for i in imports:
                ii = ActorConfig.resolve_yaml_file_inclusion(i)
                di = dict_merge(ii, di)
            return dict_merge(di, d)
        else:
            i = ActorConfig.resolve_yaml_file_inclusion(imports)
            return dict_merge(i, d)

    def __check_actor_definition_integrity(self):
        # check if the essential tags are present.
        # Essentiality of tags can be defined in a schema.
        essential_tags = [
            "toolinfo_module",
            "resourcelimits",
            "actor_name",
            "archive",
            "format_version",
        ]
        diff = essential_tags - self._config.keys()
        if diff:
            msg = (
                "The following tags are missing in the actor config YAML: \n"
                + "\n".join(diff)
            )
            sys.exit(msg)

    def __sanitize_yaml_dict(self):
        # translate resource limits
        reslim = self._config.get("resourcelimits", None)
        if reslim:
            reslim["memlimit"] = benchexec.util.parse_memory_value(reslim["memlimit"])
            reslim["timelimit"] = benchexec.util.parse_timespan_value(
                reslim["timelimit"]
            )
            self._config["resourcelimits"] = reslim

    def __resolve_url_archive(self, url):
        filename = util.get_ARCHIVE_DOWNLOAD_PATH() / (self.actor_name + ".zip")
        if not filename.is_file():
            download(url, filename.parent, filename.name)
        return str(filename)

    def __install_if_needed(self):
        target_dir = util.get_INSTALL_DIR() / self.actor_name
        # Check if the directory already exists
        if target_dir.is_dir():
            return target_dir
        archive_url = make_url(self.archive_location)
        archive_name = archive_url.rpartition("/")[2]
        if not archive_name:
            archive_name = self.actor_name + ".zip"

        archive = util.get_ARCHIVE_DOWNLOAD_PATH() / archive_name
        if not archive.is_file():
            download(archive_url, archive)
        print("Installing the actor: " + self.actor_name + "......")
        unzip(archive)

        # Get the top directory from the zip archive, and then rename it.
        # Our definition of a well formed archived means that it has only one folder at the top folder.
        with ZipFile(archive, "r") as z:
            install_path = util.get_INSTALL_DIR() / z.filelist[0].filename.split("/")[0]
            # Renaming the extracted folder to the one with actor name.
            install_path.rename(target_dir)
        return target_dir

    def __resolve_tool_info_module(self):
        """
        1. Check if it is a URL.
        2. If a URL then download it and save it to the TI cache.
        3. Infer the module name and return it.
        """
        ti = self._config["toolinfo_module"]
        if is_url(ti):
            filename = util.get_TOOL_INFO_DOWNLOAD_PATH() / ti.rpartition("/")[2]
            if not filename.is_file():
                download(ti, filename)
            ti = filename.name

        if ti.endswith(".py"):
            ti = ti.rpartition(".")[0]

        self.tool_name = ti


def dict_merge(d1, d2):
    # Supposed to update but not overwrite. Instead update.
    for k in d2.keys():
        if k in d1.keys() and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            if isinstance(d1[k], dict) and isinstance(d2[k], dict):
                d1[k] = dict_merge(d1[k], d2[k])
            elif isinstance(d1[k], dict) or isinstance(d2[k], dict):
                # TODO this could be and XOR
                # We raise an error when one of the values is a dict, but not the other.
                msg = "YAML file could not be parsed. Clash in the tag: %r" % k
                sys.exit(msg)
            else:
                d1[k] = d2[k]
        else:
            d1[k] = d2[k]

    return d1
