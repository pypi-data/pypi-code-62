import setuptools

setuptools.setup(name="replemail",
    version="0.3.1",
    description="API for https://repl.email",
    long_description='API for https://repl.email',
    url="https://github.com/AgeOfMarcus/replemail",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['requests']
)