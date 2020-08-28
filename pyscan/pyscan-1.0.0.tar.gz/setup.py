from setuptools import *

kwargs = {
    "author" : "BrainDisassembly",
    "author_email" : "braindisassm@gmail.com",
    "description" : "Python scanner using the Nmap library",
    "entry_points" : {"console_scripts" : ["pyscan=pyscan.pyscan:main"]},
    "license" : "GPL v3",
    "name" : "pyscan",
    "packages" : ["pyscan"],
    "version" : "V1.0.0",
}

setup(**kwargs)
