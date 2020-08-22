from setuptools import setup, find_packages

EXCLUDE_FROM_PACKAGES = [
    'env*',
]

setup(name='pyplanet_agones',
    version='0.2.3',
    description='Connects PyPlanet with Agones',
    url='https://github.com/LudusMatchMaking/pyplanet_agones',
    author='Jonathan Hertz',
    author_email='jonathan_hertz2@live.dk',
    license='MIT',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=[
        'pyplanet',
        'requests'
    ],
    zip_safe=False)