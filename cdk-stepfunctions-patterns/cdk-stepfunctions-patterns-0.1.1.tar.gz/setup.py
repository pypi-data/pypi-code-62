import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-stepfunctions-patterns",
    "version": "0.1.1",
    "description": "A set of Step Functions high-level patterns.",
    "license": "MIT",
    "url": "https://github.com/kolomied/cdk-stepfunctions-patterns#readme",
    "long_description_content_type": "text/markdown",
    "author": "Dmitry Kolomiets<kolomied@amazon.co.uk>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/kolomied/cdk-stepfunctions-patterns.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "Talnakh.StepFunctions.Patterns",
        "Talnakh.StepFunctions.Patterns._jsii"
    ],
    "package_data": {
        "Talnakh.StepFunctions.Patterns._jsii": [
            "cdk-stepfunctions-patterns@0.1.1.jsii.tgz"
        ],
        "Talnakh.StepFunctions.Patterns": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda>=1.49.1, <2.0.0",
        "aws-cdk.aws-stepfunctions-tasks>=1.49.1, <2.0.0",
        "aws-cdk.aws-stepfunctions>=1.49.1, <2.0.0",
        "aws-cdk.core>=1.49.1, <2.0.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.11.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
