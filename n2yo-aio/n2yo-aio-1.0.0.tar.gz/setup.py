import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='n2yo-aio',
    version='1.0.0',
    author='Federico A. Corazza',
    author_email='federico.corazza@live.it',
    description='Asynchronous Python wrapper for the N2YO API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.facorazza.com/facorazza/n2yo-aio',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
