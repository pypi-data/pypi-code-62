from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name="vkmix",
    version="1.1",
    author="alekssamos",
    author_email="aleks-samos@yandex.ru",
    url="https://github.com/alekssamos/vkmix/",
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description=open(join(dirname(__file__), "README.MD"), encoding="UTF8").read(),
)
