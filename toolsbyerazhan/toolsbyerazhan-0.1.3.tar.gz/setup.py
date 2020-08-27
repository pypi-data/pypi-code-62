from setuptools import setup, find_packages

setup(
    name = "toolsbyerazhan",
    version = "0.1.3",
    keywords = ( "toolsbyerazhan","timetools","gputools"),
    description = "tools tutorial",
    long_description = "python tools tutorial",
    license = "MIT Licence",

    url = "https://github.com/erazhan/CommonTools",
    author = "erazhan",
    author_email = "erazhan@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["tensorflow==2.2.0"]
)
