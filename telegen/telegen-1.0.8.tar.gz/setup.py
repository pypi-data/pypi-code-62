import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()


pkg_info = {}
with open("telegen/__init__.py", "r") as f:
    module_info = exec(f.read(), pkg_info)


setuptools.setup(
    name="telegen",
    version=pkg_info["__version__"],
    author="Alessandro Cerruti",
    author_email="strychnide@protonmail.com",
    description="A CLI tool that generates code by parsing the Telegram Bot API page",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/strychnide/telegen",
    project_urls={
        "Documentation": "https://strychnide.gitlab.io/telegen",
        "Issues": "https://gitlab.com/strychnide/telegen/-/issues",
        "Source": "https://gitlab.com/strychnide/telegen",
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
    ],
    packages=setuptools.find_packages(include=["telegen", "telegen.*"]),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=["lxml"],
    extras_require={
        "doc": ["sphinx", "sphinx_rtd_theme"],
    },
    entry_points={"console_scripts": ["telegen=telegen.cli:main"]},
)
