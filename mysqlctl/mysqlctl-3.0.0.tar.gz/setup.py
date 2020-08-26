from setuptools import setup
import setuptools

setup(
    # 包名称
    name = 'mysqlctl',
    # 版本
    version = '3.0.0',
    # 作者
    author = '王哈哈',
    # 作者邮箱
    author_email = 'mail65656@163.com',
    # 描述
    description = '用于操作mysql',
    # 长描述
    long_description = "用于操作mysql",
    # 让setuptools自动发现包
    packages = setuptools.find_packages(),
    # 平台
    platforms = "any",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    # 依赖的包
    install_requires = [
        "pymysql"
    ]
)
