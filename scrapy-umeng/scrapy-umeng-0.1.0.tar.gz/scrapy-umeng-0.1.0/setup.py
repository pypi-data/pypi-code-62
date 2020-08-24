from setuptools import setup, find_packages

setup(
    name = "scrapy-umeng",
    version = "0.1.0",
    keywords = ["pip", "datacanvas", "eds", "xiaoh"],
    description = "umeng sdk for scrapy",
    long_description = "umeng sdk for scrapy",
    license = "MIT Licence",

    url = "https://github.com/geek-dc/scrapy-umeng",
    author = "derekchan",
    author_email = "dchan0831@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests']
)


