import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vizdxp",
    version="0.0.1",
    author="vinoth sukumaran",
    author_email="vsuku15@gmail.com",
    description="Simple data visualization web app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vinothsuku/vizdxp",
    packages=setuptools.find_packages(),
    install_requires=['streamlit==0.65.2', 'pandas==1.1.0', 'numpy==1.19.1', 'plotly==4.9.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
