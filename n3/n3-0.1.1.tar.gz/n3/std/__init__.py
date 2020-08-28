import os
from pathlib import Path


def trim_name(name):
    return name.split('.')[0].replace('_', '-').title().replace('-', '')


def _read_file(f):
    with open(f, encoding='utf-8') as f:
        return f.read()


root_dir = os.path.dirname(__file__)

externs = {trim_name(f.name): str(f)
           for f in Path(root_dir).rglob(r'[A-Za-z]*.py')}
sources = {trim_name(f.name): _read_file(f)
           for f in Path(root_dir).rglob(r'*.n3')}
