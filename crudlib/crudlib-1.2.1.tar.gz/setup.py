# https://pypi.org/project/crudlib/

from os.path import abspath, dirname, join

from setuptools import find_packages, setup

install_reqs = [req.strip() for req in open(abspath(join(dirname(__file__), 'requirements.txt')))]

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

# distribution:
# pip install wheel twine setuptools
# python setup.py sdist bdist_wheel
# twine upload dist/*

setup(
    name="crudlib",
    version="1.2.1",
    author="Zheng",
    author_email="zxyful@gmail.com",
    description="One API, More Database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/zxyle/crudlib",
    packages=find_packages(),
    install_requires=install_reqs,
    # tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
