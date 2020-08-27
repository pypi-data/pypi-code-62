from setuptools import setup
  
setup(  
    name='winsystem',  
    version='1.0.8',  
    description='Control Windows volume,use Windows TTS,make link on Windows，调用tts，创建快捷方式，控制音量',  
    classifiers=["Development Status :: 4 - Beta","Environment :: Win32 (MS Windows)",
                 "Intended Audience :: System Administrators","License :: Free For Home Use",
                 "Natural Language :: English","Operating System :: Microsoft :: Windows :: Windows 10"
                 ,"Operating System :: Microsoft :: Windows :: Windows 7","Programming Language :: Python :: 3 "
                 ,"Topic :: System :: Systems Administration"],  
    requires=["pywin32"],
    long_description="""
from winsystem import Volume,Speaker
Volume.Volume_control().SetVolUp(100)
Speaker.TTStalk("你好! hello ! ")
""",
    author='Wei Bo 韦博',  
    url='https://pypi.org/project/winsystem',  
    author_email='weibo19801379165@yeah.net',   
    packages=["winsystem"],    
    include_package_data=False,  
    zip_safe=True,  
)  
