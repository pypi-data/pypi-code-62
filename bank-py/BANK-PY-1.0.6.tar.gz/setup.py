import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BANK-PY", # Replace with your own username
    version="1.0.6",
    author="José Alexsandro",
    author_email="eujosealexsandro@gmail.com",
    description="Armazene Seu Dados Sem Perde nada :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://starcomicstar.weebly.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
