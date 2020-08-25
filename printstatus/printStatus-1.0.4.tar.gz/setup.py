from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.md') as file:
        return(file.read())

setup(name='printStatus',
      version='1.0.4',
      description='Display a progress bar and the status of a job in the console',
      long_description_content_type="text/markdown",
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
      ],
      url='https://abittner.gitlab.io/home/',
      author='Adrian Bittner',
      author_email='adrian.bittner@eso.org',
      license='Other/Proprietary License',
      packages=find_packages(),
      install_requires=[],
      python_requires='>=3',
      include_package_data=True,
      zip_safe=False)
