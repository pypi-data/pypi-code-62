from setuptools import setup, find_packages

setup(
  name='flask-rest-crud',         
  packages=find_packages(),   
  version='0.0.1',      
  license='MIT',        
  description='Generate full CRUD from mongoengine models',   
  author='Rafael Corradini da Cunha',                   
  author_email='rafacunhadini@gmail.com',      
  url='https://github.com/user/rafaelcorradini/flask-rest-crud',   
  keywords=['flask', 'mongoengine', 'crud', 'rest'],   
  install_requires=[            
    'flask',
    'mongoengine'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)