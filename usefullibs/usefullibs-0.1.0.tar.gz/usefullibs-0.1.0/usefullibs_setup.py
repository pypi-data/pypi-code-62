from setuptools import setup, find_packages
import sys
sys.argv = ['usefullibs_setup.py', 'sdist', 'bdist_wheel']
long = """
a useful package for doing a lot of things with Python and for developers.
"""
setup(
    name="usefullibs", # Replace with your own username
    version="0.1.0",
    author="Allen Sun",
    author_email="allen.haha@hotmail.com",
    description="a useful package.",
    long_description=long,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['cryptography>=3.0',
                      'pyperclip>=1.8.0',
                      'requests>=2.24.0',
                      'python-whois>=0.7.3',
                      'beautifulsoup4>=4.9.1'
                      ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
