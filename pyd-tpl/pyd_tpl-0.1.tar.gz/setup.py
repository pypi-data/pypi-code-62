#encoding:utf-8
import os
import io
from setuptools import setup, find_packages

project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
data_dict = {}

def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            filename)
    if os.path.exists(filepath):
        return io.open(filepath, encoding="utf-8").read()
    else:
        return ''

for root, directory, filenames in os.walk(project_name):
    for f in filenames:
        filename = os.path.join(root, f)
        if filename.endswith("tpl"):
            if root in data_dict:
                data_dict[root].append(filename)
            else:
                data_dict[root] = [filename]

data_files = list(data_dict.items())

setup(
    name=project_name,
    version="0.1",
    url="https://github.com/yafeile/pyd_tpl",
    author="Cat",
    keywords=("pyd generate","pyd templates"),
    description="pyd generate tools",
    long_description=read_file('pyd/README.md'),
    platforms="any",
    install_requires=['Jinja2 >=2.11.2'],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'pyd-tpl=pyd_tpl.pyd_tpl:main',
        ],    
    },
    include_package_data=True,
    packages = find_packages()
)

