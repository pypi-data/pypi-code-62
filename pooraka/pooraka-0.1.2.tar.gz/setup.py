from distutils.core import setup

setup(
    name='pooraka',
    version='0.1.2',
    author='chakkritte',
    author_email='chakkritt60@nu.ac.th',
    packages=['pooraka'],
    url='https://github.com/chakkritte/pooraka',
    scripts=[],
    description='Pytorch wrapper',
    install_requires=[
        "torchvision",
        "torch",
    ],
)