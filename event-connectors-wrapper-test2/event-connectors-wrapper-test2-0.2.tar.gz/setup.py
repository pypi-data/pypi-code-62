from setuptools import setup

setup(
    name='event-connectors-wrapper-test2',
    url='https://github.com/tykiblood/kafka-wrapper',
    author='OMR',
    author_email='ingesql1992@hotmail.com',
    packages=['kafka_utils'],
    install_requires=['confluent-kafka==1.3.0'],
    version='0.2',
    license='MIT',
    description='A package to handle event driven engines',
    long_description=open('README.txt').read(),
)