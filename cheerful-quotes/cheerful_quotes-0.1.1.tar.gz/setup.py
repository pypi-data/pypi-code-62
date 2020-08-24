from distutils.core import setup

download_url = 'https://github.com/Gaobaofogo/cheerful_quotes/archive/v0.1.tar.gz'

setup(
    name='cheerful_quotes',
    packages=['cheerful_quotes'],
    version='0.1.1',
    license='MIT',
    description='Devolve um toque de tranquilidade via mensagens',
    author='Gabriel Augusto',
    author_email='gabrieldiniz54@gmail.com',
    url='https://github.com/Gaobaofogo',
    download_url=download_url,
    keywords=['quotes', 'cheerful'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.5',
    ],
)
