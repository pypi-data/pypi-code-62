try:
    from setuptools import setup, Extension
except:
    from distutils import setup, Extension

ext_modules = [
    Extension(
        "libpymath.testModule",
        ["LibPyMath/LibPyMathModules/testModule.c"],
    )
]

setup(
    name="libpymath",
    version="0.0.1",
    description="A general purpose Python math module",
    long_description="",
    author="Toby Davis",
    author_email="pencilcaseman@gmail.com",
    url="https://www.github.com/pencilcaseman/gpc",
    ext_modules=ext_modules,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
