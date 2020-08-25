import os
from distutils.dir_util import copy_tree


def create_brics_base():
    # create base brics folder
    if not os.path.exists('./brics'):
        from_directory = './lib/bric_builder/brics'

        copy_tree(from_directory, './brics')


def create_bric(name):
    # check if base exists
    create_brics_base()

    # copy subdirectory example

    to_directory = os.path.join('./brics/', name)
    if not os.path.exists(to_directory):
        os.mkdir(to_directory)
    else:
        return

    from_directory = './lib/bric_builder/template'

    copy_tree(from_directory, to_directory)
