import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="number-helper",
    version="0.0.2",
    author="Ha Hao minh",
    author_email="minhhahao@gmail.com",
    description="A small number helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minhhahao/number-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)