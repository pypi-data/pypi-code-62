from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='preadwrite',
    version='0.0.1',
    author='Nohhyun Park',
    author_email='nohhyun.park@gmail.com',
    license='MIT License',
    description='pread, pwrite interface for pypy 6.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    cffi_modules=["preadwrite/preadwrite_build.py:ffibuilder"],
    packages=['preadwrite'],
    install_requires=["cffi>=1.0.0"],
    setup_requires=["cffi>=1.0.0"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Operating System',
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
