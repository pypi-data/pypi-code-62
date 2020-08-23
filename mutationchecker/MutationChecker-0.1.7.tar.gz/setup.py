from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup (
    name="MutationChecker", 
    author="RMolina",
    author_email="ruben.molina-fernandez@upf.edu",
    version="0.1.7",
    description="Package for the computation of distances from a residue to the catalytic active residues.",
    packages= ["MutationChecker"],
    requirements = [
        "biopython", 
        "requests"
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
exit()
