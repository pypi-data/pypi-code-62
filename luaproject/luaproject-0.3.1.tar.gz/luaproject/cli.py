import os
import click
from fastutils import fsutils
from fastutils import strutils


def report(file_replaced, file_failed, clean_name):
    for filename in file_replaced:
        print("file {}, replace example to {} done.".format(filename, clean_name))
    for filename, error in file_failed.items():
        print("file {}, replace example to {} failed, error message: {}".format(filename, clean_name, str(error)))

@click.group()
def main():
    pass

@main.command()
@click.option("-v", "--version", default="0.1.0-1")
@click.argument("lua-package-name", required=True)
@click.argument("dst-path", required=False)
def init(version, lua_package_name, dst_path):
    """Init lua project.
    """
    if not dst_path:
        dst_path = lua_package_name
    clean_name = lua_package_name.replace("-", "_")

    # copy template to target folder
    example_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "example"))
    fsutils.copy(example_path, dst_path, keep_src_folder_name=False)
    
    # rename package example
    example_app_path = os.path.abspath(os.path.join(dst_path, "example"))
    dst_app_path = os.path.abspath(os.path.join(dst_path, clean_name))
    fsutils.rename(example_app_path, dst_app_path)
    
    # rename manage filename
    manage_example_path = os.path.abspath(os.path.join(dst_path, "manage_example.py"))
    dst_manage_example_path = os.path.abspath(os.path.join(dst_path, "manage_" + clean_name + ".py"))
    fsutils.rename(manage_example_path, dst_manage_example_path)

    # replace files' content
    file_replaced, file_failed = fsutils.file_content_replace(dst_manage_example_path, "example", clean_name)
    report(file_replaced, file_failed, clean_name)

    # replace files' content
    file_replaced, file_failed = fsutils.file_content_replace(dst_path, "example", clean_name)
    report(file_replaced, file_failed, clean_name)

    # replace files' content
    file_replaced, file_failed = fsutils.file_content_replace(dst_path, clean_name + "-manager", lua_package_name + "-manager")
    report(file_replaced, file_failed, clean_name)

    # replace files' content
    class_name = strutils.camel(lua_package_name, clean=True)
    file_replaced, file_failed = fsutils.file_content_replace(dst_path, "Example", class_name)
    report(file_replaced, file_failed, class_name)


if __name__ == "__main__":
    main()

