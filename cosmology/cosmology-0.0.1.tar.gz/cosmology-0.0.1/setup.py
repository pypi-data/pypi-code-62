import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cosmology',
    version='0.0.1',
    author='Nicolas Tessore',
    author_email='nicolas.tessore@manchester.ac.uk',
    description='a package for cosmology',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ntessore/cosmology',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
