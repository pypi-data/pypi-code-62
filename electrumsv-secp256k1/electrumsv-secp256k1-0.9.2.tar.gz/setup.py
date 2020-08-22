import errno
import os
import os.path
import platform
import shutil
import subprocess
import tarfile
from distutils import log
from distutils.command.build_clib import build_clib as _build_clib
from distutils.command.build_ext import build_ext as _build_ext
from io import BytesIO
import sys

from setuptools import Distribution as _Distribution, setup, find_packages, __version__ as setuptools_version
from setuptools.command.egg_info import egg_info as _egg_info
from setuptools.command.sdist import sdist as _sdist

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    _bdist_wheel = None


sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from setup_support import absolute, build_flags, detect_dll


BUILDING_FOR_WINDOWS = detect_dll()

MAKE = 'gmake' if platform.system() in ['FreeBSD'] else 'make'

# Version of libsecp256k1 to download if none exists in the `libsecp256k1`
# directory
LIB_TARBALL_URL = 'https://github.com/electrumsv/secp256k1/archive/314a61d72474aa29ff4afba8472553ad91d88e9d.tar.gz'


# We require setuptools >= 3.3
if [int(i) for i in setuptools_version.split('.', 2)[:2]] < [3, 3]:
    raise SystemExit(
        'Your setuptools version ({}) is too old to correctly install this '
        'package. Please upgrade to a newer version (>= 3.3).'.format(setuptools_version)
    )


def download_library(command):
    if command.dry_run:
        return
    libdir = absolute('libsecp256k1')
    if os.path.exists(os.path.join(libdir, 'autogen.sh')):
        # Library already downloaded
        return
    if not os.path.exists(libdir):
        command.announce('downloading libsecp256k1 source code', level=log.INFO)
        try:
            import requests

            r = requests.get(LIB_TARBALL_URL, stream=True)
            status_code = r.status_code
            if status_code == 200:
                content = BytesIO(r.raw.read())
                content.seek(0)
                with tarfile.open(fileobj=content) as tf:
                    dirname = tf.getnames()[0].partition('/')[0]
                    tf.extractall()
                shutil.move(dirname, libdir)
            else:
                raise SystemExit(f'Unable to download secp256k1 library: HTTP-Status: {status_code}')
        except requests.exceptions.RequestException as e:
            raise SystemExit(f'Unable to download secp256k1 library: {e}')


class egg_info(_egg_info):
    def run(self):
        # Ensure library has been downloaded (sdist might have been skipped)
        download_library(self)

        _egg_info.run(self)


class sdist(_sdist):
    def run(self):
        download_library(self)
        _sdist.run(self)


if _bdist_wheel:
    class bdist_wheel(_bdist_wheel):
        def run(self):
            download_library(self)
            _bdist_wheel.run(self)
else:
    bdist_wheel = None


class build_clib(_build_clib):
    def initialize_options(self):
        _build_clib.initialize_options(self)
        self.build_flags = None

    def finalize_options(self):
        _build_clib.finalize_options(self)
        if self.build_flags is None:
            self.build_flags = {'include_dirs': [], 'library_dirs': [], 'define': []}

    def get_source_files(self):
        # Ensure library has been downloaded (sdist might have been skipped)
        download_library(self)

        return [
            absolute(os.path.join(root, filename))
            for root, _, filenames in os.walk(absolute('libsecp256k1'))
            for filename in filenames
        ]

    def build_libraries(self, libraries):
        raise Exception('build_libraries')

    def check_library_list(self, libraries):
        raise Exception('check_library_list')

    def get_library_names(self):
        return build_flags('libsecp256k1', 'l', os.path.abspath(self.build_temp))

    def run(self):
        build_temp = os.path.abspath(self.build_temp)

        try:
            os.makedirs(build_temp)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(absolute('libsecp256k1/configure')):
            # configure script hasn't been generated yet
            autogen = absolute('libsecp256k1/autogen.sh')
            os.chmod(absolute(autogen), 0o755)
            subprocess.check_call([autogen], cwd=absolute('libsecp256k1'))

        for filename in [
            'libsecp256k1/configure',
            'libsecp256k1/build-aux/compile',
            'libsecp256k1/build-aux/config.guess',
            'libsecp256k1/build-aux/config.sub',
            'libsecp256k1/build-aux/depcomp',
            'libsecp256k1/build-aux/install-sh',
            'libsecp256k1/build-aux/missing',
            'libsecp256k1/build-aux/test-driver',
        ]:
            try:
                os.chmod(absolute(filename), 0o755)
            except OSError as e:
                # some of these files might not exist depending on autoconf version
                if e.errno != errno.ENOENT:
                    # If the error isn't 'No such file or directory' something
                    # else is wrong and we want to know about it
                    raise

        cmd = [
            absolute('libsecp256k1/configure'),
            '--disable-shared',
            '--enable-static',
            '--disable-dependency-tracking',
            '--with-pic',
            '--enable-module-recovery',
            '--disable-jni',
            '--prefix',
            os.path.abspath(self.build_clib),
            '--enable-experimental',
            '--enable-module-ecdh',
            '--enable-benchmark=no',
            #  '--enable-endomorphism',
        ]

        log.debug('Running configure: {}'.format(' '.join(cmd)))
        subprocess.check_call(cmd, cwd=build_temp)

        subprocess.check_call([MAKE], cwd=build_temp)
        subprocess.check_call([MAKE, 'install'], cwd=build_temp)

        self.build_flags['include_dirs'].extend(build_flags('libsecp256k1', 'I', build_temp))
        self.build_flags['library_dirs'].extend(build_flags('libsecp256k1', 'L', build_temp))


class build_ext(_build_ext):
    def run(self):
        if self.distribution.has_c_libraries():
            _build_clib = self.get_finalized_command('build_clib')
            self.include_dirs.append(os.path.join(_build_clib.build_clib, 'include'))
            self.include_dirs.extend(_build_clib.build_flags['include_dirs'])

            self.library_dirs.insert(0, os.path.join(_build_clib.build_clib, 'lib'))
            self.library_dirs.extend(_build_clib.build_flags['library_dirs'])

            self.define = _build_clib.build_flags['define']

        return _build_ext.run(self)


if BUILDING_FOR_WINDOWS:
    class Distribution(_Distribution):
        def is_pure(self):
            return False

    setup_kwargs = dict(
        package_data={'electrumsv_secp256k1': ['*.dll']},
        include_package_data=True,
    )
else:
    class Distribution(_Distribution):
        def has_c_libraries(self):
            return True

    setup_kwargs = dict(
        setup_requires=['cffi>=1.3.0', 'requests'],
        ext_package='electrumsv_secp256k1',
        cffi_modules=['_cffi_build/build.py:ffi'],
        cmdclass={
            'build_clib': build_clib,
            'build_ext': build_ext,
            'egg_info': egg_info,
            'sdist': sdist,
            'bdist_wheel': bdist_wheel,
        },
    )


setup(
    name='electrumsv-secp256k1',
    version='0.9.2',

    description='Cross-platform Python libsecp256k1 for ElectrumSV',
    long_description=open('README.rst', 'r').read(),
    author='Roger Taylor',
    author_email='roger.taylor.email@gmail.com',
    maintainer='Roger Taylor',
    maintainer_email='roger.taylor.email@gmail.com',
    url='https://github.com/electrumsv/electrumsv-secp256k1',
    download_url='https://github.com/electrumsv/electrumsv-secp256k1',
    license='MIT/Apache-2.0',

    install_requires=['cffi>=1.3.0'],

    packages=find_packages(exclude=('_cffi_build', '_cffi_build.*', 'libsecp256k1',)),

    distclass=Distribution,
    zip_safe=False,

    keywords=(
        'secp256k1',
        'crypto',
        'elliptic curves',
        'bitcoin',
        'bitcoin-sv',
        'bitcoin sv',
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security :: Cryptography',
    ],
    **setup_kwargs
)
