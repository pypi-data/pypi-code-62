import setuptools

setuptools.setup(
    name = 'coralinede',
    version = '1.0.1',
    license='MIT',
    description = 'python library for data engineering',
    author = 'coraline tech',
    author_email = 'tech@coraline.co.th',
    url = 'https://github.com/coralinetech/coralinede',
    download_url = '',
    keywords = ['data-engineering', 'pandas', 'python', 'pandas-helper'],
    packages=setuptools.find_packages(include=['coralinede', 'coralinede.*']),
    install_requires=[
            'sqlalchemy',
            'pandas',
            'numpy'
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
    ],
)
