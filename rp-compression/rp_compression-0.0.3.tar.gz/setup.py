from setuptools import setup, find_packages

setup(
    name='rp_compression',
    version='0.0.3',
    description='gradient compression with random projection',
    author='SangMook Kim',
    author_email='sangmook.kim@kaist.ac.kr',
    url='https://github.com/ElvinKim/rp_compression',
    install_requires=['torch', 'numpy'],
    packages=find_packages(exclude=[]),
    keywords=['gradient', 'compression', 'random', 'projection'],
    python_requires='>=3',
    package_data={},
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],
)
