from setuptools import setup, find_packages
import sys
sys.argv = ['html_setup.py', 'sdist', 'bdist_wheel']
long = """
simple html access using python only
"""
setup(
    name="simple_html5", # Replace with your own username
    version="1.0",
    author="Allen Sun",
    author_email="allen.haha@hotmail.com",
    description="HTML5",
    long_description=long,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
