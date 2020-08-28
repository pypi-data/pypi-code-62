"""
Filter CXI file by dataset values
Author: Sergey Bobkov
"""

import os
from typing import Optional, Tuple
import numpy as np
from . import cxidata


def filter_file(input_file: str, output_file: str, filter_dset_name: str,
                min_value: Optional[float], max_value: Optional[float]) -> Tuple[int, int]:
    """Filter CXI file by filter_dset_name. Filter selection is: min <= values <= max.
    Selection is applied to all datasets with same length as filter dataset.

    Keyword arguments:
    input_file -- input CXI files
    output_file -- output CXI file
    filter_dset_name -- path to filter dataset (relative to image_N/)
    min_value -- minimal selected value. If None - not applied.
    max_value -- maximum selected value. If None - not applied.

    Return:
    total_num -- total number of elements in file
    selected_num -- number of selected elements
    """

    image_ids = cxidata.get_image_groups(input_file)

    if not image_ids:
        raise ValueError('No data in CXI file: {}'.format(input_file))

    cxidata.create_file(output_file)

    total_num = 0
    selected_num = 0

    for image_id in image_ids:
        names = cxidata.get_names(input_file, image_id)

        if filter_dset_name not in names:
            raise ValueError("Dataset '{}' does not exist in image {} file {}".format(
                filter_dset_name, image_id, input_file))

        filter_data = cxidata.read_dataset(input_file, image_id, filter_dset_name)

        if filter_data.ndim != 1:
            raise ValueError("Filter dataset should have 1D shape, found: {}".format(
                filter_data.shape))

        filter_len = filter_data.shape[0]
        selection = np.ones(filter_len, dtype=np.bool)

        if min_value is not None:
            selection = np.logical_and(selection, filter_data >= min_value)

        if max_value is not None:
            selection = np.logical_and(selection, filter_data <= max_value)

        total_num += filter_len
        selected_num += selection.sum()

        if selection.sum() == 0:
            continue

        output_image_id = cxidata.add_image_group(output_file)

        _filter_image(input_file, image_id, output_file, output_image_id, selection)

    if selected_num == 0:
        os.remove(output_file)

    return total_num, selected_num


def _filter_image(input_file: str, input_image_id: int, output_file: str, output_image_id: int,
                  selection: 'np.ndarray[np.bool]') -> None:
    for name in cxidata.get_names(input_file, input_image_id):
        shape = cxidata.get_dataset_shape(input_file, input_image_id, name)
        compression = cxidata.get_dataset_compression(input_file, input_image_id, name)
        chunks = cxidata.get_dataset_chunks(input_file, input_image_id, name)
        dtype = cxidata.get_dataset_dtype(input_file, input_image_id, name)

        ndim = len(shape)
        chunk_size = int(1e8 // (np.prod(shape[1:]) + 1) + 1)

        if ndim == 0:
            data = cxidata.read_dataset(input_file, input_image_id, name)
            cxidata.save_dataset(output_file, output_image_id, name, data)
        elif shape[0] == len(selection):
            cxidata.create_dataset(output_file, output_image_id, name,
                                   (selection.sum(),) + shape[1:], dtype, chunks, compression)

            for start in range(0, shape[0], chunk_size):
                end = min(start + chunk_size, shape[0])

                if selection[start:end].sum() == 0:
                    continue

                data = cxidata.read_dataset(input_file, input_image_id, name, start, end)
                data = data[selection[start:end]]

                out_start = selection[:start].sum()
                out_end = selection[:end].sum()
                cxidata.update_dataset(output_file, output_image_id, name, data,
                                       out_start, out_end)
        else:

            cxidata.create_dataset(output_file, output_image_id, name, shape, dtype,
                                   chunks, compression)

            for start in range(0, shape[0], chunk_size):
                end = min(start + chunk_size, shape[0])

                data = cxidata.read_dataset(input_file, input_image_id, name, start, end)
                cxidata.update_dataset(output_file, output_image_id, name, data, start, end)
