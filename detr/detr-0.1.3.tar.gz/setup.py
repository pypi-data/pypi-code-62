from setuptools import setup, find_packages, find_namespace_packages

NAME = 'detr'

setup(
    name=NAME,
    version='0.1.3',
    description='See facebookresearch/detr on GitHub',

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    namespace_packages=[], #find_namespace_packages(),
    install_requires=['torch>=1.5.0', 'torchvision>=0.6.0']
)
