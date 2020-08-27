
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="helloCasechhavi",
    version="1.0.0",
    descp="The hello world package",
    long_descp=long_description,
    long_descp_content="text/markdown",
    author="Chhavi Trivedi",
    authoremail="chhavi7320@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["newPackage"],
    include_package_data=True,
    # install_requires=,
    entry_points={
        "console_scripts": [
            "py_case=newPackage.__main__:main",
        ]
    },
)
