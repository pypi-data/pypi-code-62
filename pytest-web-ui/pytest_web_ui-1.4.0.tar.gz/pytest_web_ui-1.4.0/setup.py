"""Setup script for PyTest web UI."""
import setuptools


def main():
    with open("README.md") as f:
        long_description = f.read()

    setuptools.setup(
        name="pytest_web_ui",
        version="1.4.0",
        author="Ryan Collingham",
        author_email="ryanc118@gmail.com",
        description="An interactive web UI test runner for PyTest",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ryanc414/pytest_web_ui",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 7 - Inactive",
        ],
        python_requires=">=3.6",
        install_requires=["pytest-commander"],
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
