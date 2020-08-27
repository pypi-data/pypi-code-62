from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "lonny_flask_auth",
        version = "1.9",
        packages = find_packages(),
        install_requires = f.read().splitlines()
    )