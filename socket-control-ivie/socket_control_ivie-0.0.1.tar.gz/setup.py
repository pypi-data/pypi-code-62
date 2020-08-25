from setuptools import setup

with open ("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='socket_control_ivie',
    version='0.0.1',
    description='controls sockets using python',
    py_modules=["socket_control"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        'dev':[
            "twine",
        ],
    },
    
)