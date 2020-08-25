import setuptools


setuptools.setup(
    name='spherical-dev',

    use_scm_version=True,
    setup_requires=[
        'setuptools_scm',
    ],

    author='Anton Patrushev',
    author_email='ap@spherical.pm',
    maintainer='spherical.pm',
    maintainer_email='support@spherical.pm',

    description='Set of tools used in Spherical development',
    license='MIT',

    packages=[
        'spherical.dev',
    ],
    package_dir={
        '': 'src',
    },
    namespace_packages=[
        'spherical',
    ],
    extras_require={
        'dev': [
            'invoke',
            'flake8',
            'isort',
            'pytest-cov',
            'pytest',
        ],
    },
    zip_safe=True,
)
