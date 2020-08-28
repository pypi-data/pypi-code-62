# coding: utf8

import ast
from setuptools import setup


def readme():
    with open('README.rst', 'rb') as f:
        return f.read().decode('UTF-8')


def version():
    path = 'pypika/__init__.py'
    with open(path, 'rU') as file:
        t = compile(file.read(), path, 'exec', ast.PyCF_ONLY_AST)
        for node in (n for n in t.body if isinstance(n, ast.Assign)):
            if len(node.targets) == 1:
                name = node.targets[0]
                if isinstance(name, ast.Name) and \
                        name.id in ('__version__', '__version_info__', 'VERSION'):
                    v = node.value
                    if isinstance(v, ast.Str):
                        return v.s

                    if isinstance(v, ast.Tuple):
                        r = []
                        for e in v.elts:
                            if isinstance(e, ast.Str):
                                r.append(e.s)
                            elif isinstance(e, ast.Num):
                                r.append(str(e.n))
                        return '.'.join(r)


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name="XPyPika",
    version=version(),
    author="Timothy Heys",
    author_email="theys@kayak.com",
    license='Apache License Version 2.0',
    packages=["pypika"],
    include_package_data=True,
    url="https://github.com/kayak/pypika",
    description="A SQL query builder API for Python",
    long_description=readme(),
    install_requires=required,
    test_suite="pypika.tests",
)
