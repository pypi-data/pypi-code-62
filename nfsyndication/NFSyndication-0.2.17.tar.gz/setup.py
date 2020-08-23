""" Setup for NFSyndication
 See: https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

from os.path import dirname, abspath, join, exists
from setuptools import setup, find_packages
from NFSyndication import __version__

with open("README.rst", "r") as fh:
    long_description = fh.read()
 
install_reqs = [req for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

setup(
    name = "NFSyndication",
    version = __version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [ 
            'nfsyndication-src = NFSyndication.config:init',
            'nfsyndication-releasecss = NFSyndication.config:hold_stylesheet'            
         ]
        },
    package_data = {'NFSyndication': ['templates/*.html']},
    description= "News Feed Syndication - A package that read and fetch RSS feeds from the publications.",
    long_description=long_description,
    author = "Web SRC",
    author_email = "web.system.management@gmail.com",
    install_requires=install_reqs,
    license = "GNU GPL",
    keywords = "rss, news",
    project_urls={ 
        'Source': 'https://github.com/web-sys1/NFSyndication/'
    }
)
