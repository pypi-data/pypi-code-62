import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apigram", # Replace with your own username
    version="0.0.2",
    author="andprokofieff",
    author_email="prokofieff.help@gmail.com",
    description="Python library to make bot with Telegram Bot API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andprokofieff/apigram",
    packages=['apigram'],
    install_requires=['requests', 'enum34;python_version<"3.4"', 'six'],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.4',
)