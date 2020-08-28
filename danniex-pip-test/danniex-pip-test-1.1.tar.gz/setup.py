from setuptools import setup, find_packages

setup(
    name='danniex-pip-test',  # 打包后的包文件名
    version='1.1',  # 版本号
    author='xiongdanni',
    author_email='xpanda2518@gmail.com',
    description='just a test package',  # 说明
    long_description='none',  # 详细说明
    license="MIT Licence",  # 许可
    url='', # 一般是GitHub项目路径
    keywords=("test", "client"),  # 关键字
    # packages=find_packages(),     #这个参数是导入目录下的所有__init__.py包
    #include_package_data = True,
    #platforms = "any",
    #install_requires = ['thrift'],  # 引用到的第三方库
    # py_modules=['pip-test.DoRequest', 'pip-test.GetParams', 'pip-test.ServiceRequest',
    #             'pip-test.ts.constants', 'pip-test.ac.Agent2C',
    #             'pip-test.ts.ttypes', 'pip-test.ac.constants',
    #             'pip-test.__init__'],  # 你要打包的文件，这里用下面这个参数代替
    packages = ['pip-test']  # 这个参数是导入目录下的所有__init__.py包
)