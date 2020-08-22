from distutils.core import setup
setup(
    name = 'release-dir-scanner',
    packages = ['release_dir_scanner'],
    version = '1.0.1',
    description = 'Python module for detecting audio releases in a directory structure',
    url = 'https://github.com/spiritualized/release-dir-scanner',
    download_url = 'https://github.com/spiritualized/release-dir-scanner/archive/v1.0.1.tar.gz',
    keywords = ['music', 'python', 'scanner', 'management'],
    install_requires = [],

    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
