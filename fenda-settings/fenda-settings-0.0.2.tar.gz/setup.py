import setuptools

setuptools.setup(
    name="fenda-settings",
    version="0.0.2",
    author="rejown",
    author_email="rejown@gmail.com",
    description="Fenda Settings",
    long_description='fenda settings',
    long_description_content_type="text/markdown",
    url="https://fenda.io/ff/settings",
    packages=['fenda.settings'],
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
    ],
    tests_require=[
        'pytest',
    ],
)
