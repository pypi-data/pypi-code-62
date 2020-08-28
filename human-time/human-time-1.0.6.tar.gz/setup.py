from setuptools import setup, find_packages


def readme():
    with open("README.md") as readmeFile:
        return readmeFile.read()


setup(
    name="human-time",
    version="1.0.6",
    author="Jonathan Neill",
    author_email="jonnyneill@hotmail.com",
    description="Converts digit based time formats to the english language equivalent",
    keywords="talking clock human time",
    license='MIT',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jonnyneill/human-time",
    include_package_data=True,
    packages=find_packages(),
    install_requires=["connexion[swagger-ui]"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "humantime=src.cli_client:main",
            "humantime-server=src.app:start"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
    ],
)
