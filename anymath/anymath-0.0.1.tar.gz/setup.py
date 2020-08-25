import setuptools

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anymath", 
    version="0.0.1",
    author="Рябов Никита",
    author_email="riabovnick080@yandex.ru",
    description="tool for work witn any number systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikita-080/anymath-0.0.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
