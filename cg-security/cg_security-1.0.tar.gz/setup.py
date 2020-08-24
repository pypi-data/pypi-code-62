from setuptools import setup, find_packages

setup(
    name='cg_security',
    version="1.0",
    author="Connect Group, Roberto Mizuuti",
    author_email="infra@connect.com.vc",
    url="https://github.com/ConnectSW/cg_security",
    packages=find_packages(),
    install_requires=[
        "pycryptodome"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)