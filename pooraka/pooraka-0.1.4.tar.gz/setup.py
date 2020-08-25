from distutils.core import setup

setup(
    name='pooraka',
    version='0.1.4',
    author='Chakkrit Termritthikun',
    author_email='chakkritt60@nu.ac.th',
    packages=['pooraka'],
    url='https://github.com/chakkritte/pooraka',
    scripts=[],
    description='Pytorch wrapper',
    install_requires=['torch >= 1.0', 'torchvision'],
    python_requires='>=3.6',
)