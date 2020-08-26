import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ASLMutation", # Replace with your own username
    version="1.0.0",
    author="Yunhao Zhang",
    author_email="zhangyunhao.wangjie@bytedance.com",
    description="ASL Mutation library used by DevOps in ByteDance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.byted.org/devops/process-component",
    packages=setuptools.find_packages(),
    install_requires=[
      'js2py',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
