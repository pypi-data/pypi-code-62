import os
import click
import tempfile
from fastutils import fsutils
from fastutils import randomutils


def get_package_name(template_text):
    for line in template_text.splitlines():
        line = line.strip()
        if line.startswith("package"):
            _, name = line.split("=")
            name = name.strip()
            return name[1:-1]
    return ""

def get_version(template_text):
    for line in template_text.splitlines():
        line = line.strip()
        if line.startswith("version"):
            _, name = line.split("=")
            name = name.strip()
            return name[1:-1]
    return ""


class LuaProjectManager(object):

    def __init__(self, application, lua_source_folder="src/lua", rockspec_filename="src/.rockspec"):
        if isinstance(application, str):
            self.application_root = application
        else:
            self.application_root = os.path.abspath(os.path.dirname(application.__file__))
        self.lua_source_folder = os.path.abspath(os.path.join(self.application_root, lua_source_folder))
        self.rockspec_filename = os.path.abspath(os.path.join(self.application_root, rockspec_filename))

    def pack(self, username=None):
        current_folder = os.path.abspath(os.getcwd())
        workspace = fsutils.get_temp_workspace("lua-project-manager-")
        os.chdir(workspace)
        print("workspace=", workspace)
        template_text = fsutils.readfile(self.rockspec_filename)
        name = get_package_name(template_text)
        version = get_version(template_text)
        source_folder_name = "{0}-{1}".format(name, version)
        source_zip_name = source_folder_name + ".zip"
        dst_source_folder_path = os.path.join(workspace, source_folder_name)
        print("dst_source_folder_path=", dst_source_folder_path)
        fsutils.copy(self.lua_source_folder, dst_source_folder_path)

        cmd = "zip {0} -r {1}".format(source_zip_name, source_folder_name)
        print("command=", cmd)
        os.system(cmd)

        dst_rockspec_name = "{}-{}.rockspec".format(name, version)
        dst_rockspec_path = os.path.abspath(os.path.join(workspace, dst_rockspec_name))
        print("dst_rockspec_path=", dst_rockspec_path)
        fsutils.copy(self.rockspec_filename, dst_rockspec_path)
        
        rock_name = "{}-{}.src.rock".format(name, version)
        rock_path = os.path.abspath(os.path.join(workspace, rock_name))
        cmd = "zip {0} {1} {2}".format(rock_name, source_zip_name, dst_rockspec_name)
        print("command=", cmd)
        os.system(cmd)

        os.chdir(current_folder)
        dist_rock_path = os.path.abspath(os.path.join(current_folder, rock_name))
        fsutils.copy(rock_path, dist_rock_path)

        if username:
            rockspec_name = "{}-{}.rockspec".format(name, version)
            fsutils.copy(self.rockspec_filename, rockspec_name)
            print("copy: {} -> {}".format(self.rockspec_filename, rockspec_name))
            zip_url = "{}-{}.zip".format(name, version)
            real_url = "https://luarocks.org/manifests/{username}/{name}-{version}.src.rock".format(username=username, name=name, version=version)
            fsutils.file_content_replace(rockspec_name, zip_url, real_url)

        fsutils.rm(workspace)
        return dist_rock_path
    
    def install(self, package):
        cmd = "luarocks install {0}".format(package)
        print("command=", cmd)
        os.system(cmd)

    def get_manager(self):
        @click.group()
        def manager():
            pass


        @manager.command()
        def install():
            """Create a lua package and then install it.
            """
            package_path = self.pack()
            self.install(package_path)

        @manager.command()
        @click.option("-u", "--username", required=False)
        def pack(username):
            """Create a lua package.
            """
            self.pack(username)

        return manager

