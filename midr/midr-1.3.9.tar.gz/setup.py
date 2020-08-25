#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import setuptools
import sys
import os
import re
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

# class CMakeExtension(Extension):
#     def __init__(self, name, cmake_lists_dir='.', **kwa):
#         Extension.__init__(
#             self,
#             name,
#             sources=[],
#             **kwa
#         )
#         self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)
#
# class cmake_build_ext(build_ext):
#     def build_extensions(self):
#         # Ensure that CMake is present and working
#         try:
#             out = subprocess.check_output(['cmake', '--version'])
#         except OSError:
#             raise RuntimeError('Cannot find CMake executable')
#
#         for ext in self.extensions:
#             extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
#             cfg = 'Release'
#
#             cmake_args = [
#                 '-DCMAKE_BUILD_TYPE=%s' % cfg,
#                 # Ask CMake to place the resulting library in the directory
#                 # containing the extension
#                 '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
#                 # Other intermediate static libraries are placed in a
#                 # temporary build directory instead
#                 '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), self.build_temp),
#                 # Hint CMake to use the same Python executable that
#                 # is launching the build, prevents possible mismatching if
#                 # multiple versions of Python are installed
#                 '-DPYTHON_EXECUTABLE={}'.format(sys.executable),
#                 # Add other project-specific CMake arguments if needed
#                 # ...
#             ]
#
#             # We can handle some platform-specific settings at our discretion
#             if platform.system() == 'Windows':
#                 plat = ('x64' if platform.architecture()[0] == '64bit' else 'Win32')
#                 cmake_args += [
#                     # These options are likely to be needed under Windows
#                     '-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE',
#                     '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
#                 ]
#                 # Assuming that Visual Studio and MinGW are supported compilers
#                 if self.compiler.compiler_type == 'msvc':
#                     cmake_args += [
#                         '-DCMAKE_GENERATOR_PLATFORM=%s' % plat,
#                     ]
#                 else:
#                     cmake_args += [
#                         '-G', 'MinGW Makefiles',
#                     ]
#
#             if not os.path.exists(self.build_temp):
#                 os.makedirs(self.build_temp)
#
#             # Config
#             subprocess.check_call(['cmake', ext.cmake_lists_dir] + cmake_args,
#                                   cwd=self.build_temp)
#
#             # Build
#             subprocess.check_call(['cmake', '--build', '.', '--config', cfg],
#                                   cwd=self.build_temp)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="midr",
    version="1.3.9",
    packages=['midr'],
    python_requires=">=3.6",
    install_requires=[
        'cmake>=3.18'
        'scipy>=1.3',
        'numpy>=1.16',
        'pynverse>=0.1',
        'pandas>=0.25.0',
        'mpmath>=1.1.0',
        'matplotlib>=3.0.0'
    ],
    author="Laurent Modolo",
    author_email="laurent.modolo@ens-lyon.fr",
    description="Compute idr from m NarrowPeak files and a merged NarrowPeak",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitbio.ens-lyon.fr/LBMC/sbdm/midr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, \
version 2.1 (CeCILL-2.1)",
        "Operating System :: OS Independent"
    ],
    test_suite='pytest',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['midr=midr.__main__:main'],
    },
    ext_modules=[CMakeExtension('c_archimedean')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False
)

