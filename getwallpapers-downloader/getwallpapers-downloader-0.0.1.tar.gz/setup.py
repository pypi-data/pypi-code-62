from setuptools import setup, find_packages
from io import open

setup(
    name='getwallpapers-downloader',
    version='0.0.1',
    description='Download wallpapers from getwallpapers.com',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/falcon-head/getwallpapers-downloader',
    author='Aptha K S',
    author_email='iamuraptha@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4','tqdm','urllib3'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
