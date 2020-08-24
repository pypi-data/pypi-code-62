from distutils.core import setup
setup(
    name='revns',
    packages=['revns'],
    version='0.3',
    license='MIT',
    description='notification service for revteltech',
    author='Chien Hsiao',
    author_email='chien.hsiao@revteltech.com',
    url='https://github.com/revtel/rns',
    download_url='https://github.com/revtel/revns/archive/v0.3.tar.gz',
    keywords=['revteltech', 'notification'],
    install_requires=[
        'django',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
