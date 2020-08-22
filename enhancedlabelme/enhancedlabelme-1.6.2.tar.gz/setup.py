from __future__ import print_function


import re
from setuptools import find_packages
from setuptools import setup
import distutils.spawn
import shlex
import subprocess
import sys


def get_version():
    filename = 'enhancedlabelme/__init__.py'
    with open(filename, encoding='utf-8') as f:
        match = re.search(
            r'''^__version__ = ['"]([^'"]*)['"]''', f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    PY3 = sys.version_info[0] == 3
    PY2 = sys.version_info[0] == 2
    assert PY3 or PY2

    install_requires = [
        "imgviz>=0.11.0",
        "matplotlib",
        "numpy",
        "Pillow>=2.8.0",
        "PyYAML",
        "qtpy",
        "termcolor",
        'QDarkStyle>=2.8.1',
        'pynput',
        "colorama",
        "requests",
        "PyQt5>=5.15.0",
    ]

    # Find python binding for qt with priority:
    # PyQt5 -> PySide2 -> PyQt4,
    # and PyQt5 is automatically installed on Python3.
    QT_BINDING = None

    try:
        import PyQt5  # NOQA
        QT_BINDING = 'pyqt5'
    except ImportError:
        pass

    if QT_BINDING is None:
        try:
            import PySide2  # NOQA
            QT_BINDING = 'pyside2'
        except ImportError:
            pass

    if QT_BINDING is None:
        try:
            import PyQt4  # NOQA
            QT_BINDING = 'pyqt4'
        except ImportError:
            if PY2:
                print(
                    'Please install PyQt5, PySide2 or PyQt4 for Python2.\n'
                    'Note that PyQt5 can be installed via pip for Python3.',
                    file=sys.stderr,
                )
                sys.exit(1)
            assert PY3
            # PyQt5 can be installed via pip for Python3
            install_requires.append('PyQt5')
            QT_BINDING = 'pyqt5'
    del QT_BINDING

    return install_requires


def get_long_description():
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
    try:
        import github2pypi
        return github2pypi.replace_url(
            slug='wkentaro/labelme', content=long_description
        )
    except Exception:
        return long_description


def main():
    version = get_version()

    if sys.argv[1] == 'release':
        if not distutils.spawn.find_executable('twine'):
            print(
                'Please install twine:\n\n\tpip install twine\n',
                file=sys.stderr,
            )
            sys.exit(1)

        commands = [
            'python tests/docs_tests/man_tests/test_labelme_1.py',
            'git tag v{:s}'.format(version),
            'git push origin master --tag',
            'python setup.py sdist',
            'twine upload dist/enhancedlabelme-{:s}.tar.gz'.format(version),
        ]
        for cmd in commands:
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name='enhancedlabelme',
        version=version,
        packages=find_packages(),
        description='Image Polygonal Annotation with Python',
        long_description=get_long_description(),
        long_description_content_type='text/markdown',
        author='Kentaro Wada',
        author_email='www.kentaro.wada@gmail.com',
        url='https://github.com/wkentaro/labelme',
        install_requires=get_install_requires(),
        license='GPLv3',
        keywords='Image Annotation, Machine Learning',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
        package_data={'enhancedlabelme': ['icons/*', 'config/*.yaml', 'ui/*', '*.md']},
        entry_points={
            'console_scripts': [
                'labelme+=enhancedlabelme.__main__:main',
                'labelme+_draw_json=enhancedlabelme.cli.draw_json:main',
                'labelme+_draw_label_png=enhancedlabelme.cli.draw_label_png:main',
                'labelme+_json_to_dataset=enhancedlabelme.cli.json_to_dataset:main',
                'labelme+_on_docker=enhancedlabelme.cli.on_docker:main',
            ],
        },
        data_files=[('share/man/man1', ['docs/man/labelme.1'])],
    )


if __name__ == '__main__':
    main()
