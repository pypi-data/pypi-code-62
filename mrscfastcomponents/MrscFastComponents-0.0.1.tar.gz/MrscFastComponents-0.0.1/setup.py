from setuptools import find_packages, setup
from distutils.extension import Extension
import Cython.Compiler.Options
from Cython.Build import cythonize

Cython.Compiler.Options.annotate = True

extensions = [Extension(name="BasicComponents/*", sources=["BasicComponents/*.pyx"])]

cythonize_setup = cythonize(extensions,
                            # annotate=True,
                            compiler_directives={"language_level": 3,
                                                 "boundscheck": False,
                                                 "wraparound": False})

setup(
    name="MrscFastComponents",
    version='0.0.1',
    description="Fast Multi-Robot Sorting Centers Components for Prototyping.",
    ext_modules=cythonize_setup,
    author="Chee-Henn Chng",
    author_email="cheehennchng@gmail.com",
    classifiers=["License :: OSI Approved :: MIT License"]
)
