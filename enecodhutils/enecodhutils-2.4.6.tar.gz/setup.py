from setuptools import setup, find_packages

setup(
    name='enecodhutils',
    version='2.4.6',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A python package containing all the boiler plate code for Eneco-datahub utils.',
    long_description='add read me later',
    install_requires=['requests', 'pykafka', 'pyodbc', 'pandas', 'deprecated',
                      'retrying', 'azure-common', 'azure-storage'],
    author='Dharmateja Yarlagadda',
    author_email='dharmateja.yarlagadda@eneco.com'
)