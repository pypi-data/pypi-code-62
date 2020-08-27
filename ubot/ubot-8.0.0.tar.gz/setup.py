import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="ubot",
    version="8.0.0",
    author="Alessandro Cerruti",
    author_email="strychnide@protonmail.com",
    description="A CLI tool that generates code by parsing the Telegram Bot API page",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/strychnide/ubot",
    project_urls={
        "Documentation": "https://strychnide.gitlab.io/ubot",
        "Issues": "https://gitlab.com/strychnide/ubot/-/issues",
        "Source": "https://gitlab.com/strychnide/ubot",
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=setuptools.find_packages(include=["ubot"]),
    python_requires=">=3.6",
    # fmt: off
    extras_require={
        "doc": ["sphinx", "sphinx_rtd_theme"],
        "dev": ["black"],
        "test": ["telegen-definitions"]
    },
    # fmt: on
)
