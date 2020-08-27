import setuptools
from setuptools import setup, Extension

'''
 打包需要按如下方式配置工程
  .
├── README.md 
├── __init__.py
├── gt_push_sdk
│   ├── BatchImpl.py
│   ├── GtConfig.py
│   ├── RequestException.py
│   ├── __init__.py
│   ├── google
│   ├── igetui
│   └── protobuf
└── setup.py
注意切换工程根目录后需要调整improt的绝对路径，否则会有importError
完成后执行 python setup.py build打包，
执行 python setup.py install下载打包结果用于测试，
执行 python setup.py sdist生成分发包
'''


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gt-push-sdk",
    version="4.1.1.1",
    author="Getui",
    author_email="gtpushsdk@gmail.com",
    description="Getui\'s officially supported Python3 client library",
    keywords=['GeTui', 'GTPush API', 'Android Push', 'iOS Push'],
    license='MIT License',

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://docs.getui.com/getui/server/python3/start/",
    packages=setuptools.find_packages(),
    platforms='any',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["certifi", "chardet", "cycler", "idna", "kiwisolver", "matplotlib", "numpy", "pip", "protobuf",
                      "pycuber", "pyparsing", "python-dateutil", "requests", "setuptools", "six", "urllib3", "wheel"]
)
