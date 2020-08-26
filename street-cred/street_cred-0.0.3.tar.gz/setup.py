from setuptools import find_packages, setup


setup(
    name='street_cred',
    version='0.0.3',
    author="Aaron Mangum",
    packages=find_packages(),
    install_requires=[
        'cryptography~=2.9',
        'psycopg2-binary~=2.8.5',
        'sqlalchemy~=1.3.15',
    ],
)
