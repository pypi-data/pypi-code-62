from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.forms.wizard'
version = '0.2'
readme = open(join('src', 'dolmen', 'forms', 'wizard', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    "grokcore.component",
    "megrok.pagetemplate",
    "setuptools",
    "zeam.form.base >= 1.4.1",
    "zeam.form.ztk >= 1.4",
    "zeam.form.layout",
    "zope.i18n",
    "zope.i18nmessageid",
    "zope.interface",
    ]

tests_require = [
    "lxml",
    "grokcore.layout",
    "zope.annotation",
    "zope.authentication",
    "zope.browserpage",
    "zope.password",
    "zope.app.appsetup",
    "zope.app.publication",
    "zope.app.wsgi[test]",
    "zope.component",
    "zope.principalregistry",
    "zope.publisher",
    "zope.schema",
    "zope.security",
    "zope.securitypolicy",
    "zope.testing",
    "zope.traversing",
    "zope.testbrowser",
    ]

setup(name=name,
      version=version,
      description=("Wizard for zeam.form"),
      long_description = readme + "\n\n" + history,
      keywords="Zeam Grok Dolmen Wizard",
      author="Christian Klinger",
      author_email="cklinger@novareto.de",
      url="",
      license="GPL",
      package_dir={"": "src"},
      packages=find_packages("src", exclude=["ez_setup"]),
      namespace_packages=["dolmen", "dolmen.forms"],
      include_package_data=True,
      zip_safe=False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {"test": tests_require},
      test_suite="dolmen.forms.wizard",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Zope3",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
          ],
      )
