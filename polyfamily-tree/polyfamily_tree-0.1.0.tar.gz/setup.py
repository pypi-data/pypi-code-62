import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polyfamily_tree",
    version="0.1.0",
    author="grasshopperTrainer",
    author_email="grasshoppertrainer@gmail.com",
    description="Python package for structuredly managing directional relationship between objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grasshopperTrainer/polyfamily_tree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='DAG, directed, acyclic, graph',
    python_requires='>=3'
)
