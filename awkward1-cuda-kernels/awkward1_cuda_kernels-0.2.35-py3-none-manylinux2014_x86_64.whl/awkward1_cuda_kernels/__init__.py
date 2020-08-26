# BSD 3-Clause License; see https://github.com/scikit-hep/awkward1/blob/master/LICENSE

from __future__ import absolute_import

import os.path
import glob

directory, filename = os.path.split(__file__)

shared_library_path = None
for filename in glob.glob(os.path.join(directory, "*awkward-cuda-kernels.*")):
    shared_library_path = filename

del os
del glob
del directory
del filename

__version__ ='0.2.35'
cuda_version ='9.0'
docker_image ='docker.io/nvidia/cuda:9.0-devel-ubuntu16.04'
