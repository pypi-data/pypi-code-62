"""
Combine several CXI files into one, combine datasets when possible
Author: Sergey Bobkov
"""

from shutil import copy2
from typing import List, Dict, Tuple
import numpy as np
from . import cxidata


def combine_files(input_files: List[str], output_file: str) -> None:
    """Combine several CXI files into one, combining datasets that
    have matching shapes.

    Keyword arguments:
    input_files -- list of input CXI files
    output_file -- filename for output CXI file
    """
    if not input_files:
        raise ValueError('Empty input_files list')

    if len(input_files) == 1:
        copy2(input_files[0], output_file)
        return

    image_id_mapping = _create_image_id_mapping(input_files)

    cxidata.create_file(output_file)

    for i in sorted(set(image_id_mapping.values())):
        output_image_id = cxidata.add_image_group(output_file)
        assert i == output_image_id

        # Select input image groups for current output image group
        input_image_groups = [key for key, val in image_id_mapping.items()
                              if val == output_image_id]

        dataset_names = []
        for fname, image_id in input_image_groups:
            dataset_names.extend(cxidata.get_names(fname, image_id))
        dataset_names = set(dataset_names)

        for name in dataset_names:
            dataset_image_groups = [(fname, image_id) for fname, image_id in input_image_groups
                                    if name in cxidata.get_names(fname, image_id)]

            _combine_dataset(name, dataset_image_groups, output_file, output_image_id)


def _combine_dataset(name: str, dataset_image_groups: List[Tuple[str, int]],
                     output_file: str, output_image_id: int) -> None:
    first_fname, first_image_id = dataset_image_groups[0]
    compression = cxidata.get_dataset_compression(first_fname, first_image_id, name)
    chunks = cxidata.get_dataset_chunks(first_fname, first_image_id, name)

    if name in ['mask', 'image_center']:
        data = cxidata.read_dataset(first_fname, first_image_id, name)
        cxidata.save_dataset(output_file, output_image_id, name, data,
                             chunks=chunks, compression=compression)
        return

    dataset_shapes = [cxidata.get_dataset_shape(fname, image_id, name)
                      for fname, image_id in dataset_image_groups]

    ndim = len(dataset_shapes[0])

    if ndim == 0:
        data = [cxidata.read_dataset(fname, image_id, name)
                for fname, image_id in dataset_image_groups]

        if all(d == data[0] for d in data):
            data = data[0]
        else:
            data = np.array(data)
        cxidata.save_dataset(output_file, output_image_id, name, data)
    elif ndim == 1:
        for j, shape in enumerate(dataset_shapes):
            if len(shape) != 1:
                fname, image_id = dataset_image_groups[j]
                raise ValueError("Dataset '{}' have incompatible shapes {} and {}".format(
                    name, dataset_shapes[0], shape))

        data = np.concatenate([cxidata.read_dataset(fname, image_id, name)
                               for fname, image_id in dataset_image_groups])
        cxidata.save_dataset(output_file, output_image_id, name, data)
    else:
        element_shape = dataset_shapes[0][1:]

        lenght = 0
        for j, shape in enumerate(dataset_shapes):
            lenght += shape[0]
            if shape[1:] != element_shape:
                fname, image_id = dataset_image_groups[j]
                raise ValueError("Dataset '{}' have incompatible shapes {} and {}".format(
                    name, dataset_shapes[0], shape))

        chunk_size = int(1e8 // (np.prod(element_shape) + 1) + 1)

        dtype = cxidata.get_dataset_dtype(first_fname, first_image_id, name)
        cxidata.create_dataset(output_file, output_image_id, name,
                               (lenght,) + element_shape, dtype, chunks, compression)

        running_length = 0
        for j, shape in enumerate(dataset_shapes):
            fname, image_id = dataset_image_groups[j]

            for start in range(0, shape[0], chunk_size):
                end = min(start + chunk_size, shape[0])

                data = cxidata.read_dataset(fname, image_id, name, start, end)
                cxidata.update_dataset(output_file, output_image_id, name, data,
                                       running_length + start, running_length + end)

            running_length += shape[0]

        assert running_length == lenght


def _create_image_id_mapping(input_files: List[str]) -> Dict[Tuple[str, int], int]:
    """ Create mapping between input files and image_id in output_file

    Keyword arguments:
    input_files -- list of input CXI files

    Return:
    image_id_mapping -- Dict with mapping (input_file, image_id) -> image_id in output file
    """
    image_keys = []
    image_id_mapping = {}

    for fname in input_files:
        file_image_ids = cxidata.get_image_groups(fname)
        for image_id in file_image_ids:
            dset_names = cxidata.get_names(fname, image_id)

            if 'mask' in dset_names:
                mask = cxidata.read_dataset(fname, image_id, 'mask')
            else:
                mask = None

            if 'image_center' in dset_names:
                image_center = cxidata.read_dataset(fname, image_id, 'image_center')
            else:
                image_center = None

            for i, key in enumerate(image_keys):
                saved_mask, saved_center = key
                if saved_mask is None and mask is None:
                    mask_fit = True
                elif saved_mask is not None and mask is not None and \
                    saved_mask.shape == mask.shape and \
                    (saved_mask == mask).all():
                    mask_fit = True
                else:
                    mask_fit = False

                if saved_center is None and image_center is None:
                    center_fit = True
                elif saved_center is not None and image_center is not None and \
                    saved_center.shape == image_center.shape and \
                    (saved_center == image_center).all():
                    center_fit = True
                else:
                    center_fit = False

                if mask_fit and center_fit:
                    image_id_mapping[(fname, image_id)] = i + 1
                    break
            else:
                image_keys.append((mask, image_center))
                image_id_mapping[(fname, image_id)] = len(image_keys)

    return image_id_mapping
