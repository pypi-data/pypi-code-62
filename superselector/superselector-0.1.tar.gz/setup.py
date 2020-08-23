from setuptools import setup, find_packages

with open('README.txt') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='superselector',
    version='0.1',
    description='A module to help you easily make arrow key selection menus in Python.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n',
    license='MIT',
    packages=find_packages(),
    author='Boyne G',
    author_email='bgamestudios@mail.com',
    keywords=['Menus', 'Selector', 'Arrows'],
    url='http://bgamestudios.tk',
    download_url='https://pypi.org/project/superselector/'
)

install_requires = [
    'keyboard',
    'colorama'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)