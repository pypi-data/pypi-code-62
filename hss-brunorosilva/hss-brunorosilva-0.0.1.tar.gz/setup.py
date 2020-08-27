from setuptools import setup
import setuptools

setup(
    name = 'hss-brunorosilva',
    version = '0.0.1',
    author='Bruno Rodrigues Silva',
    author_email='rodriguessilvabruno@outlook.com',
    description="command line interface for setting up streamlit webapps on heroku",
    url = 'https://github.com/brunorosilva/heroku-streamlit-setup',
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'hss = hss.__main__:main'
        ],
    },
    python_requires='>=3.6'
)