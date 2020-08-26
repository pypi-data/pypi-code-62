import setuptools
setuptools.setup(
    name='GeneralCartesianProduct',
    version='0.1.1',
    author='Floyd Z',
    author_email='floyd.zweydinger+github@rub.de',
    packages=['generalcartesianproduct', 'generalcartesianproduct.tests'],
    license='LICENSE.txt',
    description='extends the existing functionality of `itertools.product` by variable limits.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    url="https://github.com/FloydZ/generalcartesianproduct",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
