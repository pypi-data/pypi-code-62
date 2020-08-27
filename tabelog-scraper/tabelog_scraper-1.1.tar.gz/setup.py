from setuptools import setup, find_packages

setup(
    name="tabelog_scraper",
    version='1.01',
    description='食べログのスクレイピング',
    author='Kobori Akira',
    author_email='private.beats@gmail.com',
    url='https://github.com/koboriakira/tabelog_scraper',
    packages=find_packages(),
    install_require=open('requirements.txt').read().splitlines(),
    license='MIT',
)
