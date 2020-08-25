# Copyright (C) 2020 thisLight
#
# This file is part of PyDyImport.
#
# PyDyImport is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyDyImport is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyDyImport.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path


class DynamicImportedModule(object):
    """
    A stub class which is as a superclass of all dynamic imported modules.
    """
    pass


class DynamicImport(object):
    ROOTDIR = Path.cwd()
    CACHE = {}

    def __init__(self,
                 current_file_rel_path,
                 *,
                 global_cache=False,
                 cache=True,
                 env_injector=None,
                 inject_require=False):
        self.global_cache = global_cache
        self.need_cache = cache
        if cache:
            self.package_cache = {}
        self.current_file = self.ROOTDIR / current_file_rel_path
        self.parent_dir = self.current_file.parent
        self.env_injector = env_injector
        if inject_require:
            from .injector import RequireEnvInjector
            self.env_injector = RequireEnvInjector(self.env_injector)

    def require(self, package_path):
        """
        Load module from a file and return the content.
        :param package_path: str
        :return: DynamicImportedModule
        """
        real_path = self.parent_dir / package_path
        if self.global_cache and (real_path in self.CACHE):
            return self.CACHE[real_path]
        elif self.need_cache and (real_path in self.package_cache):
            return self.package_cache[real_path]
        else:
            mod_content = self.load_module_content_from(
                real_path, self.env_injector)
            mod = type('DynamicImportedModule', (DynamicImportedModule, ),
                       mod_content)
            mod.__name__ = mod_content['__name__']
            if self.global_cache:
                self.CACHE[real_path] = mod
            if self.need_cache:
                self.package_cache[real_path] = mod
            return mod

    def require_only(self, package_path, *field_names):
        """
        Load the module and only return fields which described in `field_names`. If one field doesn't exists, `getattr` will raise an error.

        ````python
        require_only = DynamicImport(__file__).require_only
        spam1, spam2, foo = require_only('./module.py', 'spam1', 'spam2', 'foo')
        ````

        :param package_path: str
        :param *field_names: List[str]
        :return: Tuple[Any, ...]
        """
        mod = self.require(package_path)
        fields = []
        for name in field_names:
            fields.append(getattr(mod, name))
        return tuple(fields)

    @staticmethod
    def load_module_content_from(path, env_injector):
        if path.is_file():
            text_b = path.read_bytes()
            binary = compile(text_b,
                             str(path.absolute()),
                             'exec',
                             optimize=True)
            new_global = {}
            if b"# inject_require" in text_b:
                from .injector import RequireEnvInjector
                env_injector = RequireEnvInjector(env_injector)
            if env_injector:
                new_global.update(env_injector(path, text_b))
            new_global.update({
                '__name__': path.name.split('.')[0],
                '__file__': str(path)
            })
            eval(binary, new_global)
            return new_global
        else:
            raise ImportError(
                "{} is not a file which can imported".format(path))
