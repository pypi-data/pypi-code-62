import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="everywhere",
    version="1.0",
    author="Simon Rovder",
    author_email="simon.rovder@gmail.com",
    description="A globaly importable thread local variable. This utility package is literally two lines of code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SimonRovder/everywhere",
    packages=['everywhere'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="GPL",
    python_requires='>=3.5',
)
