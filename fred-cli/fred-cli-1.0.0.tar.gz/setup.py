from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fred-cli',
    version='1.0.0',
    author='aamnv',
    author_email='aadithyan.manivannan@gmail.com',
    description='CLI app powered by FRED (Federal Reserve Economic Data)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aamnv/fred-cli',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'fred', 'tabulate',
    ],
    entry_points='''
        [console_scripts]
        fred=app.cli:fred
    ''',
    python_requires='>=3.6',
)