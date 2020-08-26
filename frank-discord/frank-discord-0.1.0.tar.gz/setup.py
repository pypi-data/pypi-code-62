# =====IMPORTS=====
# Third-party imports
import setuptools


with open('requirements.txt', 'r') as reqs_file:
    reqs = [line.strip() for line in reqs_file.readlines()]

setuptools.setup(
    name='frank-discord',
    version='0.1.0',
    author='Jef Roosens',
    author_email='',
    description='A modular tool for building Discord bots',
    long_description='See https://gitlab.com/Chewing_Bever/frank for details.',
    url='https://gitlab.com/Chewing_Bever/frank',
    packages=setuptools.find_packages(exclude=('tests',)),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
    install_requires=reqs,
    setup_requires=['wheel'],
)
