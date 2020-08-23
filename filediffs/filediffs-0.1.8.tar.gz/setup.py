import os

from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext
from setuptools import Extension, setup, find_packages


def scandir(dir, files=None):
    if files is None:
        files = []
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if os.path.isfile(path) and path.endswith(".pyx"):
            files.append(path.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


def makeExtension(extName):
    extPath = extName.replace(".", os.path.sep) + ".pyx"
    ext = Extension(
        extName,
        [extPath],
        include_dirs=['.'],
        # your include_dirs must contains the '.' for setup to search all the subfolder of the codeRootFolder
        language="c++",
    )
    return ext


extNames = scandir('filediffs')

extensions = [makeExtension(name) for name in extNames]


def read(f):
    """Open a file"""
    return open(f, encoding='utf-8').read()


setup(
    # package metadata
    name='filediffs',
    version='0.1.8',
    include_package_data=True,
    description="Separate two files into three files, each containing "
                "lines observed in both files/first file only/second file only. Programmed using Cython.",
    long_description=read('README.md'),
    author='Sebastian Cattes',
    author_email='sebastian.cattes@inwt-statistics.de',
    long_description_content_type="text/markdown",
    url='https://github.com/INWTlab/filediffs',
    license='MIT',

    # get packages that should be wheeled
    packages=find_packages(),

    # cython stuff
    package_data={
        'filediffs': [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("filediffs")) for f in fn]
    },
    extensions=extensions,
    ext_modules=cythonize(extensions,
                          annotate=False,
                          language_level=3,
                          compiler_directives={'embedsignature': True},  # for pytest-cython
                          ),
    cmdclass={'build_ext': new_build_ext},

    # shell script
    scripts=['bin/filediffs'],
    # requirements. paired with pyproject.toml
    requires=['cython'],
    # package info for pypi
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.8',
    ],
)
