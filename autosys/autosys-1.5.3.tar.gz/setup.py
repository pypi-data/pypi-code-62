# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosys',
 'autosys.cli',
 'autosys.cli.colors',
 'autosys.debug',
 'autosys.examples',
 'autosys.exceptions',
 'autosys.implore',
 'autosys.log',
 'autosys.math_utils',
 'autosys.parse',
 'autosys.parse.sample_data',
 'autosys.profile',
 'autosys.text_utils',
 'autosys.twitter',
 'autosys.utils',
 'autosys.web',
 'autosys.web.google',
 'autosys.web.json',
 'autosys.web.medium',
 'autosys.web.webpages']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'requests>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'autosys',
    'version': '1.5.3',
    'description': 'System Utilities for Python on macOS.',
    'long_description': '# [AutoSys][1]\n\n[![netlify badge](https://api.netlify.com/api/v1/badges/416b8ca3-82db-470f-9adf-a6d06264ca75/deploy-status)][link_netlify] [![Build Status](https://travis-ci.com/skeptycal/autosys.svg?branch=master)][link_travis]\n\n[![Twitter Follow](https://img.shields.io/twitter/follow/skeptycal.svg?style=social)][link_twitter] [![GitHub followers](https://img.shields.io/github/followers/skeptycal.svg?label=GitHub&style=social)][link_github]\n\n---\n\n### **An even more desperate way to make requests for Humans™.**\n\n-   Why does this have to suck so much?\n-   Why do my tools make me work for them?\n-   Why can\'t I ask for something I want to know and see it in a way I want to see it?\n-   Why haven\'t my tools changed in 30 years?\n-   Why do we need 100 different cryptic patchworks of messy code to get something done?\n-   Why do I have to change and contort to accomodate my tools?\n\n## _Why don\'t my tools work with the way humans think?_\n\n---\n\n### _If computers can do so much, why can\'t we do any of the things we want to do?_ That is the question that we seek to answer with **_Implore_**.\n\n---\n\n[![test coverage](https://img.shields.io/badge/test_coverage-100%25-6600CC.svg?logo=Coveralls&color=3F5767)](https://coveralls.io) ![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/3454/badge)\n\n### **Integrates easily in a simple, human way with:**\n\n-   Google Calendars, Contacts, Drive, Docs, Sheets\n-   Dictionaries, References, and language tools\n-   Analyze news for fake stories and spoofs\n-   Professional Journal searches\n-   Linux/macOS Command Line\n-   simple image edits and pdfs\n-   and nearly any public API\n-   Latex / BibTex documents\n-   macOS Text Messaging\n-   Common web browsers\n-   Microsoft Excel, Word\n-   Reference formatting\n-   Text Messaging\n-   NLP Processes\n-   Apple iTunes\n-   Blog Posts\n-   Youtube\n-   Netflix\n\n_Tell your computer what to do!"_\n\n> Copyright © 2018-2020 [Michael Treanor](https:/skeptycal.github.com) | [MIT License](https://opensource.org/licenses/MIT) - enjoy ...\n\n[![License](https://img.shields.io/badge/License-MIT-darkblue)](https://skeptycal.mit-license.org/1976/) [![macOS Version](https://img.shields.io/badge/macOS-10.15%20Catalina-orange?logo=apple)](https://www.apple.com) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?logo=prettier)](https://github.com/prettier/prettier)\n\n---\n\n## Implore (with Autosys) version 0.4.4\n\n### Features include:\n\n-   **Send text messages** based on results and presets\n-   Figure out the annoying **Netflix** recommendations\n-   **Watch** for cookies and other local security issues\n-   **Research** topics based on logic and language\n-   **NLP analysis** of web pages or sets of pages\n-   Test **API** functionality and build an interface\n-   Perform spoof analysis and **fact checking**\n-   **Block** specific activities of certain sites\n-   **Convert** websites to 3d object visuals\n-   Timing social media and blog **posts**\n-   Interact with underlying **database**\n-   Create a **command line** interface\n-   **Parse** html and language results\n-   Watch **Twitter** for specific topics\n-   Create link and image **catalogs**\n-   Collect **metadata** and tag info\n-   **Google Calendar** automation\n-   **Collect** website html code\n-   **Timestamp** html versions\n-   Direct Request from user\n-   Create visual **sitemaps**\n-   Calendar **reminders**\n-   **CSS** Updating\n-   **Scripting**\n-   **BibTex**\n-   **Time**\n\n_Implore requires Python 3.8+ and works best with **lxml** (fast html) and **ujson** (fast json) installed. Text messaging requires macOS._\n\n[![GitHub Pipenv locked Python version](https://img.shields.io/badge/Python-3.8-yellow?color=3776AB&logo=python&logoColor=yellow)](https://www.python.org/) ![Django v3](https://img.shields.io/badge/Django-v3-%23092E20?logo=django&color=#339933)\n\n---\n\n## Contributing\n\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)\n\n**Please feel free to offer suggestions and changes** (contribution instructions below). I have been coding for many years, but mostly as a side activity ... as a tool to assist me in other endeavors ... so I have not had the \'hard time\' invested of constant coding that many of you have.\n\n---\n\n## A solid foundation\n\n> Implore uses _Requests_ and _Beautiful Soup_ to parse html and scrape web data. Website output if mostly _Flask_ based. The majority of other functionality is original code.\n\n---\n\n## Requests: HTTP for Humans™\n\n![Requests graphic](images/requests-sidebar.jpg)\n\n_Requests is an elegant and simple HTTP library for Python, built for human beings._\n\n[Requests Documentation](https://requests.readthedocs.io/en/master/)\n\n> Requests allows you to send HTTP/1.1 requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100% automatic, thanks to urllib3.\n\n#### Beloved Features\n\n_Requests is ready for today’s web._\n\n-   Keep-Alive & Connection Pooling\n-   International Domains and URLs\n-   Sessions with Cookie Persistence\n-   Browser-style SSL Verification\n-   Automatic Content Decoding\n-   Basic/Digest Authentication\n-   Elegant Key/Value Cookies\n-   Automatic Decompression\n-   Unicode Response Bodies\n-   HTTP(S) Proxy Support\n-   Multipart File Uploads\n-   Streaming Downloads\n-   Connection Timeouts\n-   Chunked Requests\n-   .netrc Support\n\n---\n\n## Beautiful Soup\n\n![Beautiful Soup graphic](images/bs4.png)\n\n_Elixir and Tonic_\n"The Screen-Scraper\'s Friend"\n[Beautiful Soup Documentation](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)\nCopyright (c) 2004-2019 Leonard Richardson\nMIT License\n\n> Beautiful Soup uses a pluggable XML or HTML parser to parse a (possibly invalid) document into a tree representation. Beautiful Soup provides methods and Pythonic idioms that make it easy to navigate, search, and modify the parse tree.\n\n---\n\n## Flask\n\n![Flask](images/flask.png)\n\n_Web development, one drop at a time_\n[Flask Documentation](https://palletsprojects.com/p/flask/)\n\n> Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.\n\n[1]: (https://www.github.com/skeptycal/autosys)\n[link_netlify]: (https://app.netlify.com/sites/mystifying-keller-ab5658/deploys)\n[link_travis]: (https://travis-ci.com/skeptycal/autosys)\n[link_twitter]: (https://www.twitter.com/skeptycal)\n[link_github]: (https://www.github.com/skeptycal)\n',
    'author': 'skeptycal',
    'author_email': 'skeptycal@gmail.com',
    'maintainer': 'skeptycal',
    'maintainer_email': 'skeptycal@gmail.com ',
    'url': 'https://skeptycal.github.io/autosys',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
