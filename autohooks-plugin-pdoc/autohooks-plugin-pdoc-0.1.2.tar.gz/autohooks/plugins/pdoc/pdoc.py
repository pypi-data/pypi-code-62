# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess

from autohooks.api import error, ok, out
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.py',)


def check_pdoc_installed():
    try:
        import pdoc  # pylint: disable=unused-import
    except ImportError:
        raise Exception(
            'Could not find pdoc. Please add pdoc to your python environment'
        )


def get_pdoc_config(config):
    return config.get('tool', 'autohooks', 'plugins', 'pdoc')


def get_include_from_config(config):
    if not config:
        return DEFAULT_INCLUDE

    pdoc_config = get_pdoc_config(config)
    include = pdoc_config.get_value('include', DEFAULT_INCLUDE)

    if isinstance(include, str):
        return [include]

    return include


def get_pdoc_args(config):
    pdoc_config = get_pdoc_config(config)
    module_name = pdoc_config.get_value("module_name")
    http_dir = pdoc_config.get_value("http_dir")

    return ['pdoc', '--html', '--overwrite', f'--http-dir {http_dir}', module_name]


def precommit(config=None, **kwargs):  # pylint: disable=unused-argument
    out('Running pdoc pre-commit hook')

    check_pdoc_installed()

    include = get_include_from_config(config)
    files = [f for f in get_staged_status() if match(f.path, include)]

    if len(files) == 0:
        ok('No staged files for pdoc available')
        return 0

    with stash_unstaged_changes(files):
        try:
            subprocess.check_call(get_pdoc_args(config))
            ok('Running pdoc')
        except subprocess.CalledProcessError as err:
            error(f'Running pdoc failed with: {err}')
            raise err

        stage_files_from_status_list(files)

    return 0
