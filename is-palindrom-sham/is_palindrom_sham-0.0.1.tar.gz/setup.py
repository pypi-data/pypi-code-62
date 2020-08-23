from setuptools import setup, find_packages

setup(
    name = 'is_palindrom_sham',# while insdtalling pacakge
    version = '0.0.1',
    description = 'This is a palindrome checking function.',
    long_description = open('Readme.txt').read(),
    url = 'https://balajibetadur.github.io',
    author = 'Shashwat Mishra',
    keywords = ['palindrome','python palindrome','palindrome evaluator'],
    license = 'MIT',
    packages = ['is_palindrome_sham'],# while impoerting package
    install_requires = ['']
)