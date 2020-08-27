# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 11:04:19 2020
https://medium.com/@stackpython/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%99%E0%B8%B3-package-%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%A3%E0%B8%B2%E0%B8%AA%E0%B8%A3%E0%B9%89%E0%B8%B2%E0%B8%87%E0%B8%AD%E0%B8%B1%E0%B8%9E%E0%B8%A5%E0%B8%87-pypi-%E0%B8%AB%E0%B8%A3%E0%B8%B7%E0%B8%AD-pip-%E0%B9%83%E0%B8%AB%E0%B9%89%E0%B8%84%E0%B8%99%E0%B8%AD%E0%B8%B7%E0%B9%88%E0%B8%99%E0%B9%82%E0%B8%AB%E0%B8%A5%E0%B8%94%E0%B9%84%E0%B8%94%E0%B9%89-726a80ef51b8
https://engineering.thinknet.co.th/%E0%B8%AD%E0%B8%B1%E0%B8%9E-package-%E0%B8%82%E0%B8%B6%E0%B9%89%E0%B8%99-pip-%E0%B9%80%E0%B8%9E%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%95%E0%B8%B4%E0%B8%94%E0%B8%95%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B8%A5%E0%B8%87%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2%E0%B9%86-242bff5c6a9
@author: supakrni
"""

from setuptools import setup

def readme():
    with open('README.txt') as f:
        return f.read()
#def licenses():
#    with open('LICENSE.txt') as f:
#        return f.read()
    
setup(name='pyrmvtxt',
    version='1.1.3',
    description='Remove text in image',
    long_description=readme(),
    url="",
    author='tasund',
    author_email='supakrit.n@hotmail.com',
    license='MIT License Copyright  2020 TASUNDPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction,including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DINGS IN THE SOFTWARE.',
    install_requires=[
        'opencv-python',
        'keras-ocr',
        'pandas',
    ],
    keywords='removetextfromimage',
    packages=['pyrmvtxt'],
    package_dir={'pyrmvtxt': 'src/pyrmvtxt'}
)