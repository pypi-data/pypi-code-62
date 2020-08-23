from distutils.core import setup

setup(name='hs_test1',#对外的模块名
      version='1.0',#版本号
      description='这是allen对外发布的模块',#描述信息
      author='hs',#作者
      author_email='fengyeyouni@163.com',#邮箱
      py_modules=['my_prog.demo1','my_prog.demo2']#要发布的模块
      )