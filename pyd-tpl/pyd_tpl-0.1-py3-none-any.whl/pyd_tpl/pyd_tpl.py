# encoding:utf-8
from __future__ import unicode_literals

import argparse
import os
import sys

from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment

IS_WIN = sys.platform == "win32"
IS_PY3 = sys.version_info[0] == 3


def main(module_name="demo", module_type="c", class_name=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if IS_PY3:
        _path = os.path.join(path, "py3")
    else:
        _path = os.path.join(path, "py2")
    loader = FileSystemLoader(_path)
    env = SandboxedEnvironment(loader=loader)
    if class_name:
        tpl = env.get_template("class.tpl")
        text = tpl.render({"module_name": module_name, "class_name": class_name})
    else:
        tpl = env.get_template("demo.tpl")
        text = tpl.render({"module_name": module_name})
    # if IS_WIN:
    #     text = """#include "stdafx.h"\n{}
    #     """.format(text)
    fmt = "{}.{}"
    if module_type in ("cpp", "c++"):
        module_type = "cpp"
    else:
        module_type = "c"
    filename = fmt.format(module_name, module_type)
    with open(filename, "w") as f:
        f.write(text)
    loader = FileSystemLoader(path)
    env = SandboxedEnvironment(loader=loader)
    tpl = env.get_template("setup.tpl")
    text = tpl.render({"module_name": module_name, "module_type": module_type})
    with open("setup_{}.py".format(module_name), "w") as f:
        f.write(text)
    print("Generate Module {} success".format(module_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Pyd生成工具")
    parser.add_argument("module_name", type=str, help="模块名称")
    parser.add_argument("--module-type", type=str, default="c", choices=["c", "c++", "cpp"], required=False,
                        help="模块类型")
    parser.add_argument("--class-name", type=str, required=False, help="类名")
    args = parser.parse_args()
    module_name = args.module_name
    module_type = args.module_type.lower()
    class_name = args.class_name
    if module_name is None:
        parser.print_help()
    main(module_name, module_type, class_name)
