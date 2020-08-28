"""
Compute number of photons and litpixels in CXI file
Author: Sergey Bobkov
"""

import numpy as np
from . import cxidata


def compute_photons(filename: str, chunk_size: int = 1000) -> None:
    """Get dataset shape from CXI file

    Keyword arguments:
    filename -- name of file
    chunk_size -- number of frames processed in one chunk
    """

    image_ids = cxidata.get_image_groups(filename)

    for image_id in image_ids:
        data_shape = cxidata.get_dataset_shape(filename, image_id, 'data')
        if len(data_shape) != 3:
            raise ValueError('Data has wrong number of dimensions: {} != 3'.format(len(data_shape)))

        num_frames = data_shape[0]

        num_photons = np.zeros(num_frames)
        litpixels = np.zeros(num_frames)

        for start in range(0, num_frames, chunk_size):
            end = min(start+chunk_size, num_frames)
            chunk_data = cxidata.read_dataset(filename, image_id, 'data', start, end)
            num_photons[start:end] = np.sum(chunk_data, axis=(1, 2))
            litpixels[start:end] = np.sum(chunk_data > 0, axis=(1, 2))

        if 'num_photons' in cxidata.get_names(filename, image_id):
            cxidata.update_dataset(filename, image_id, 'num_photons', num_photons)
        else:
            cxidata.save_dataset(filename, image_id, 'num_photons', num_photons)

        if 'num_litpixels' in cxidata.get_names(filename, image_id):
            cxidata.update_dataset(filename, image_id, 'num_litpixels', litpixels)
        else:
            cxidata.save_dataset(filename, image_id, 'num_litpixels', litpixels)
