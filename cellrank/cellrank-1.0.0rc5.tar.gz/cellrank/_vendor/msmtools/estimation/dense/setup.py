
def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('dense', parent_package, top_path)

    config.add_subpackage('mle')
    config.add_subpackage('tmat_sampling')
    return config
