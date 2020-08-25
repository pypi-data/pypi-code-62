import setuptools

setuptools.setup(
    name="bric-layer",
    version="0.0.2",
    author="G B",
    description="Layer",
    long_description_content_type="text/markdown",
    url="https://github.com/bankova-gabriella/layer/",
    install_requires=[
        "numpy",
        "pandas",
        "munch",
        "docker",
        "colorlog",
        "pipey",
        "graphene",
        'SQLAlchemy',
        'azure-storage-blob',
        'xlrd',
        'pyodbc',
        'pymsteams',
        'adal',
        'cx_Oracle',
        'psycopg2',
        'pymongo',
        'elasticsearch',
        'elasticsearch[async]',
        'boto3',
        'snowflake-connector-python',
        'wheel',
        'pylint',
        'python-language-server'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

# python setup.py sdist & twine upload --repository pypi dist/*
