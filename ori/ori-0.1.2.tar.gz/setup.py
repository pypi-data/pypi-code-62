# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ori']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ori',
    'version': '0.1.2',
    'description': 'Concurrency tools for Python.',
    'long_description': 'Ori, a high-level concurrency library for Python\n=================================================\n\nOri is a high-level wrapper around Python\'s `concurrent.futures` module, designed to make multithreading and multiprocessing as easy as possible.\n\nOri modules\n-----------\n\nThe tools that Ori provides are divided into several modules.\n\n`ori.asyncio <https://ori.technology.neocrym.com/en/latest/ori.asyncio/>`_ -- Tools to integrate Python asyncio code into a synchronous codebase, and vice-versa.\n\n`ori.concurrency <https://ori.technology.neocrym.com/en/latest/ori.concurrency/>`_ -- Tools to run Python functions in the background using multithreading or multiprocessing.\n\n`ori.poolchain <https://ori.technology.neocrym.com/en/latest/ori.poolchain/>`_ -- A way to chain function calls for parallel processing over any list or other iterable.\n\n`ori.subprocess <https://ori.technology.neocrym.com/en/latest/ori.subprocess/>`_ -- Tools for running external commands as subprocesses and efficiently collecting the standard output and standard error.\n\n\nFrequently Asked Questions (FAQs)\n---------------------------------\n\n**Who made Ori?**\n\nOri was written by `James Mishra <https://jamesmishra.com>`_ and incubated at `Neocrym <https://neocrym.com>`_, a record label that uses artificial intelligence to find and promote musicians. Neocrym heavily relies on Ori to make their I/O-bound Python code run faster.\n\nThe source code for Ori is owned by Neocrym Records Inc, but licensed to Ori under the MIT License.\n\n**Why should I use Ori over directly interfacing with concurrent.futures?**\n\nThe Python module `concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html>`_ was introduced as a high-level abstraction over lower-level interfaces like `threading.Thread` and `multiprocessing.Process`. However, `concurrent.futures` merely moves the problem away from managing threads or processes to managing *executors*. Ori has the ambitious goal of also abstracting away the executors--making multithreading or multiprocessing no harder than writing single-threaded code.\n\n**Is Ori a good replacement for Python\'s asyncio?**\n\nFor the hardcore `asyncio <https://docs.python.org/3/library/concurrent.futures.html>`_ user, probably not. Ori is focused on providing high-level abstractions over Python\'s  `concurrent.futures <https://docs.python.org/3/library/concurrent.futures.html>`_ module that provides speed boosts for synchronous, I/O-bound Python.\n\n**What do I need to know to contribute to Ori?**\n\nOri manages itself with the Python packaging tool `Poetry <https://python-poetry.org/>`_. You can install Poetry on your system with:\n\n.. code:: text\n\n    pip3 install poetry\n    poetry install\n\n\nTo check that your changes to Ori\'s codebase match our coding standards, and to reformat any errant code to meet our standards, run this command:\n\n.. code:: text\n\n    poetry run make lint\n\nTo run Ori\'s unit tests in the Python virtualenv created by Poetry, just run:\n\n.. code:: text\n\n    poetry run make test\n    \nWe can also run tests across multiple versions of Python with `Tox <https://tox.readthedocs.io/en/latest/>`_, but it requres your system has `Docker <https://docs.docker.com/get-docker/>`_ and `Docker Compose <https://docs.docker.com/compose/install/>`_ installed. If so, just run:\n\n.. code:: text\n\n    poetry run make tox\n\n**Where did the name "Ori" come from?**\n\nThe name "Ori" is a reference to the god-like villains in the Stargate TV shows. There is no meaningful connection between the villains or concurrency.\n',
    'author': 'James Mishra',
    'author_email': 'james.mishra@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
