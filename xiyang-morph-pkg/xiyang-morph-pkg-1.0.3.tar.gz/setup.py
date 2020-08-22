import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiyang-morph-pkg",  # 名称为以后pip安装包的名字，后面最好加上用户名，避免名称冲突
    version="1.0.3",
    author="Xiyang",
    author_email="838568501@qq.com",
    description="morph package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires = ["dlib",  "numpy", "scipy", "opencv-contrib-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
