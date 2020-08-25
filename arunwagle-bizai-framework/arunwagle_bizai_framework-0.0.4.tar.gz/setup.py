import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arunwagle_bizai_framework",  # Replace with your own username
    version="0.0.4",
    author="Arun Wagle",
    author_email="arun.wagle@gmail.com",
    description="BizAI Framework Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['bizai.framework'],
    package_data={
        'bizai.framework': ['*', '*/*', '*/*/*'],
    },
    python_requires='>=3.6',
)
