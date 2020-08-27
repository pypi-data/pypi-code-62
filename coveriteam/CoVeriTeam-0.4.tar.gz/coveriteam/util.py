# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import os
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
import re
import urllib.request
from pathlib import Path
import shutil
import sys

LOG_DIR = Path.cwd() / "cvt-output"
TOOL_OUTPUT_FILE = "output.txt"
INPUT_FILE_DIR = f'{Path(__file__).parent.resolve() / "artifactlibrary/"}/'
ACTOR_CONFIG_PATH = ""


def set_cache_directories(d=None):
    global INSTALL_DIR, ARCHIVE_DOWNLOAD_PATH, TOOL_INFO_DOWNLOAD_PATH
    if d:
        cache_dir = d
    elif os.getenv("XDG_CACHE_HOME"):
        cache_dir = Path(os.getenv("XDG_CACHE_HOME")) / "coveriteam"
    else:
        cache_dir = Path.home() / ".cache" / "coveriteam"
    INSTALL_DIR = cache_dir / "tools"
    ARCHIVE_DOWNLOAD_PATH = cache_dir / "archives"
    TOOL_INFO_DOWNLOAD_PATH = cache_dir / "toolinfocache"
    sys.path.append(str(TOOL_INFO_DOWNLOAD_PATH))


def create_cache_directories():
    # Create directories and set path.
    if not ARCHIVE_DOWNLOAD_PATH.is_dir():
        ARCHIVE_DOWNLOAD_PATH.mkdir(parents=True)
    if not TOOL_INFO_DOWNLOAD_PATH.is_dir():
        TOOL_INFO_DOWNLOAD_PATH.mkdir(parents=True)

    if not INSTALL_DIR.is_dir():
        INSTALL_DIR.mkdir(parents=True)


def get_INSTALL_DIR():
    return INSTALL_DIR


def get_ARCHIVE_DOWNLOAD_PATH():
    return ARCHIVE_DOWNLOAD_PATH


def get_TOOL_INFO_DOWNLOAD_PATH():
    return TOOL_INFO_DOWNLOAD_PATH


def is_url(path_or_url):
    return "://" in path_or_url or path_or_url.startswith("file:")


def make_url(path_or_url):
    """Make a URL from a string which is either a URL or a local path,
    by adding "file:" if necessary.
    """
    if not is_url(path_or_url):
        return "file:" + urllib.request.pathname2url(path_or_url)
    return path_or_url


def download(url, filename):
    print("downloading from " + url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla"})
    with urllib.request.urlopen(req) as response, filename.open(  # noqa: S310
        "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)


def create_archive(dirname, archive_path):
    with ZipFile(archive_path, "w", ZIP_DEFLATED) as zipf:
        for root, _dirs, files in os.walk(dirname):
            for f in files:
                filepath = os.path.join(root, f)
                zipf.write(filepath, os.path.relpath(filepath, dirname))


def unzip(archive):
    with ZipFile(archive, "r") as zipfile:
        # Not to use extract all as it does not preserves the permission for executable files.
        for member in zipfile.namelist():
            if not isinstance(member, ZipInfo):
                member = zipfile.getinfo(member)
            extracted_file = zipfile.extract(member, INSTALL_DIR)
            attr = member.external_attr >> 16
            if attr != 0:
                os.chmod(extracted_file, attr)


def filter_dict(d, d1):
    return {k: d[k] for k in d1.keys()}


def str_dict(d):
    return {k: str(d[k]) for k in d.keys()}


def dict_clash(d1, d2):
    """
    This function checks if there is a key present in both dictionaries
    whose values are different.
    """
    for k in d1.keys():
        if k in d2.keys() and d1[k] != d2[k]:
            return True

    return False


def rename_dict(d, renaming_map):
    return {(renaming_map.get(k, None) or k): d[k] for k in d.keys()}


def collect_variables(exp):
    regex_isinstance = r"(?<=isinstance\()\S+(?=,)"
    regex_in = r"\w+(?= in \[)"
    regex = regex_isinstance + "|" + regex_in
    names = re.findall(regex, exp)

    return names


def get_additional_paths_for_container_config():
    base_dir = Path(__file__).parent.parent.resolve()
    paths = [str(base_dir / "lib"), str(base_dir / "coveriteam" / "toolconfigs")]
    return paths
