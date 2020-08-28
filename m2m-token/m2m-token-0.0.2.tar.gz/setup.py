import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="m2m-token",
    version="0.0.2",
    author="Maxime Faye",
    author_email="maxime.faye@gmail.com",
    description="Generates token for machine-to-machine authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Maskime/m2m_token",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)