import os
import numpy
from Cython.Build import cythonize


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    libraries = []
    if os.name == 'posix':
        libraries.append('m')

    config = Configuration('cluster', parent_package, top_path)
    config.add_subpackage('SNNDPC')

    config.add_extension('_agci_emb',
                         sources=['_agci_emb.pyx'],
                         include_dirs=[numpy.get_include()],
                         language="c++")

    config.add_extension('FCDMF_',
                         sources=['FCDMF_.pyx'],
                         include_dirs=[numpy.get_include()],
                         language="c++")

    config.ext_modules = cythonize(config.ext_modules, nthreads=4, compiler_directives={'language_level': 3})
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
