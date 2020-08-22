# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2020 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from ..framew.application import OperationError
from .base import BaseBuilder

##############################################################################


class CurseforgeBuilder (BaseBuilder):

    build_subloc = 'curseforge'

    default_manifest = {'minecraft': {'version': None,
                                      'modLoaders': []
                                      },
                        'manifestType': 'minecraftModpack',
                        'manifestVersion': 1,
                        'overrides': 'overrides',
                        'files': []
                        }

    ##########################################################################

    def do_build(self):
        self.log.info('Copying local files ...')
        self.copy_files(self.build_location('overrides'), self.packlock.yield_clientonly_files())

        self.log.info('Generating manifest.json ...')
        manifest = self.default_manifest
        manifest['minecraft']['version'] = self.packlock.get_metadata('minecraft_version')
        manifest['minecraft']['modLoaders'].append({'id': 'forge-{}'.format(self.packlock.get_metadata('forge_version')),
                                                    'primary': True})
        manifest['name'] = self.packlock.get_metadata('title')
        if manifest['name'] is None:
            raise OperationError('Curseforge builds require a \'title\' metadata field.')
        manifest['version'] = self.packlock.get_metadata('version')
        if manifest['version'] is None:
            raise OperationError('Curseforge builds require a \'version\' metadata field.')

        manifest['authors'] = self.packlock.get_metadata('authors')
        if manifest['authors'] is None:
            raise OperationError('Curseforge builds require an \'author\' metadata field.')

        html_modlist = '\ufeff<ul>\n'

        for mod in self.packlock.yield_clientonly_mods():
            modrecord = {'projectID': mod.projectId,
                         'fileID': mod.fileId,
                         'required': True
                         }
            manifest['files'].append(modrecord)
            html_modlist += '<li><a href="{}">{} (by {})</a></li>\n'.format(mod.website,
                                                                            mod.slug,
                                                                            mod.author)
        for rep in self.packlock.get_all_resourcepacks():
            reprecord = {'projectID': rep.projectId,
                         'fileID': rep.fileId,
                         'required': True
                         }
            manifest['files'].append(reprecord)
            html_modlist += '<li><a href="{}">{} (by {})</a></li>\n'.format(rep.website,
                                                                            rep.slug,
                                                                            rep.author)
        html_modlist += '</ul>\n'

        manifestcontent = json.dumps(manifest, indent=2)
        with open('{}/manifest.json'.format(self.build_location()), 'wt') as mf:
            mf.write(manifestcontent)

        with open('{}/modlist.html'.format(self.build_location()), 'wb') as mlf:
            mlf.write(html_modlist.encode('utf-8'))

        pkgfilename = '{}/{}-{}.{}'.format(self.release_location(),
                                           self.packlock.get_metadata('name'),
                                           self.packlock.get_metadata('version'),
                                           self.release_extension)
        self.log.info('Packaging the modpack: {} ...'.format(pkgfilename))
        self.release_pkg(pkgfilename)

##############################################################################
# THE END
