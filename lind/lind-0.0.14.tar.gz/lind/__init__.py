"""
Lind
============

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
the documentation site https://james-montgomery.github.io/project_name/.



We recommend exploring the docstrings using
`IPython <https://ipython.org>`_, an advanced Python shell with
TAB-completion and introspection capabilities.  See below for further
instructions.

The docstring examples assume that `numpy` has been imported as `np`::
  >>> import lind as ld
Code snippets are indicated by three greater-than signs::
  >>> x = 42
  >>> x = x + 1
Use the built-in ``help`` function to view a function's docstring::
  >>> help(ld.function)
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
