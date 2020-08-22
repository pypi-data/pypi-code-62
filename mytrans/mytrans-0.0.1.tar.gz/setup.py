import setuptools

with open('README.md', 'r', encoding='utf8') as rf:
    long_description = rf.read()

setuptools.setup(
    name='mytrans',
    version='0.0.1',
    author='Soul Drummer',
    author_email='function@88.com',
    description='Free Translate(google/deepl) API for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=['requests']
)