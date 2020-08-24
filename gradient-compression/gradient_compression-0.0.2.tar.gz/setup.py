from setuptools import setup, find_packages

setup(
    name='gradient_compression',
    version='0.0.2',
    description='gradient compression algorithms with PyTorch',
    author='SangMook Kim',
    author_email='sangmook.kim@kaist.ac.kr',
    url='https://github.com/ElvinKim/gradient_compression',
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
