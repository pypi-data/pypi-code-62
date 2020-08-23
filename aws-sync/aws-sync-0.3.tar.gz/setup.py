from setuptools import setup, find_packages

setup(
    name="aws-sync",
    packages=find_packages(),
    version="0.3",
    description="Sync AWS secrets across multiple accounts",
    long_description="This python package allows user to easily sync or replicate specifc or all secrets between multiple AWS accounts.",
    author="Udhav Pawar",
    author_email="upawar78@gmail.com",
    url="https://github.com/UdhavPawar/aws_sync",
    keywords=["aws","secrets","aws-secrets-manager","aws-sync","replicate","credentials","automation"],
    license="MIT",
    include_package_data = True,
    install_requires=["boto3"],
)
