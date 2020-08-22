import setuptools
import cachein

setuptools.setup(
    name="cachein",
    version=cachein.VERSION,
    author="Rich Harkins",
    author_email="rich.harkins@gmail.com",
    description="Lazy caching, delegation, and more",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hrharkins/python-cachein",
    packages=['cachein'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

