from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'pychatapp',
    packages = setuptools.find_packages(),
    version = '1.6',
    license='MIT',
    description = 'It is a chatting application written in Python, purpose of PyChatApp is to bring python community together and connect with various Pythonistas around the world.',
    author = 'Ankit Raj Mahapatra',
    author_email = 'ankitrajjitendra816@gmail.com',
    url = 'https://github.com/Ankit404butfound/pychatapp',
    #download_url = 'https://github.com/Ankit404butfound/awesomepy/archive/1.0.tar.gz',
    keywords = ['start'],
    install_requires=[
          'plyer',
          'requests',
          
      ],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
