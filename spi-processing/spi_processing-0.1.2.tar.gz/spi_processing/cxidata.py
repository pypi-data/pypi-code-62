"""
Library for CXI file operations
Author: Sergey Bobkov
"""

import os
from typing import List, Optional, Union, Tuple
import errno
import numpy as np
import h5py


def create_file(filename: str, rewrite: bool = False) -> None:
    """Create empty CXI file

    Keyword arguments:
    filename -- name of file
    rewrite -- rewrite content if file exists
    """
    if not rewrite and os.path.exists(filename):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), filename)

    with h5py.File(filename, 'w') as h5file:
        h5file['cxi_version'] = 160
        h5file.create_group('entry_1')


def add_image_group(filename: str) -> int:
    """Add image group to CXI file

    Keyword arguments:
    filename -- name of file

    Return:
    image_id -- id of created group
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    existing_ids = get_image_groups(filename)

    image_id = 1
    while image_id in existing_ids:
        image_id += 1

    with h5py.File(filename, 'a') as h5file:
        entry = h5file['entry_1']
        entry.create_group('image_{}'.format(image_id))
        entry['data_{}'.format(image_id)] = h5py.SoftLink('/entry_1/image_{}'.format(image_id))

    return image_id


def get_image_groups(filename: str) -> List[int]:
    """Get IDs of image groups in CXI file

    Keyword arguments:
    filename -- name of file

    Return:
    ids -- IDs of image groups
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        entry = h5file['entry_1']
        ids = [int(key[6:]) for key in entry.keys()
               if key.startswith('image_') and key[6:].isdigit()]

    return ids


def get_names(filename: str, image_id: int) -> List[str]:
    """Get names of all datasets in image group in CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group

    Return:
    names -- List of dataset names
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        return _get_group_content(image)


def _get_group_content(h5group: h5py.Group) -> List[str]:
    names = []
    for key in h5group.keys():
        if isinstance(h5group.get(key, getlink=True), h5py.SoftLink):
            raise ValueError('SoftLink detected, exit due to undefined behaviour')

        item = h5group[key]
        if isinstance(item, h5py.Dataset):
            names.append(key)
        elif isinstance(item, h5py.Group):
            for name in _get_group_content(item):
                names.append(key + '/' + name)

    return names


def create_dataset(filename: str, image_id: int, name: str, shape: Tuple[int, ...],
                   dtype: type, chunks: Tuple[int, ...] = None, compression: str = None) -> None:
    """Save dataset to CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    shape -- array shape
    dtype -- array data type
    chunks -- hdf chunks for created dataset
    compression -- use compression for dataset
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'a') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name in image:
            raise ValueError('Dataset {} already exists in image {}'.format(name, image_id))

        image.create_dataset(name, shape=shape, dtype=dtype, chunks=chunks, compression=compression)


def delete_dataset(filename: str, image_id: int, name: str) -> None:
    """Delete dataset from CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'a') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        del image[name]


def save_dataset(filename: str, image_id: int, name: str, data: Union[np.ndarray, str, List],
                 chunks: Tuple[int] = None, compression: str = None) -> None:
    """Save dataset to CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    data -- array with data to save
    chunks -- hdf chunks for created dataset
    compression -- use compression for dataset
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'a') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name in image:
            raise ValueError('Dataset {} already exists in image {}'.format(name, image_id))

        image.create_dataset(name, data=data, chunks=chunks, compression=compression)


def read_dataset(filename: str, image_id: int, name: str,
                 chunk_start: Optional[int] = None, chunk_end: Optional[int] = None) -> np.ndarray:
    """Read dataset from CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    chunk_start -- read chunk of data starting from chunk_start
    chunk_end -- read chunk of data ends at chunk_end

    Return:
    data -- dataset content
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        if not image[name].shape:
            return image[name][()]

        num_frames = image[name].shape[0]

        if chunk_start is None:
            chunk_start = 0

        if chunk_end is None:
            chunk_end = num_frames

        if not 0 <= chunk_start < num_frames:
            raise ValueError('Chunk_start should be >= 0 and < {}'.format(num_frames))

        if not 0 <= chunk_end <= num_frames:
            raise ValueError('Chunk_end should be >= 0 and <= {}'.format(num_frames))

        if chunk_start >= chunk_end:
            raise ValueError('Chunk_start should be < chunk_end')

        return image[name][chunk_start:chunk_end]


def update_dataset(filename: str, image_id: int, name: str, data: np.ndarray,
                   chunk_start: Optional[int] = None, chunk_end: Optional[int] = None) -> None:
    """Save dataset to CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    data -- array with data to save
    chunk_start -- update chunk of data starting from chunk_start
    chunk_end -- update chunk of data ends at chunk_end
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    if chunk_start is not None and chunk_start < 0:
        raise ValueError('Chunk_start should be >= 0')

    if chunk_end is not None and chunk_end < 0:
        raise ValueError('Chunk_end should be >= 0')

    with h5py.File(filename, 'a') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        if chunk_start is None:
            chunk_start = 0
        if chunk_end is None:
            chunk_end = len(image[name])

        update_shape = (chunk_end - chunk_start, ) + image[name].shape[1:]

        if update_shape != data.shape:
            raise ValueError('Data shape does not fit update chunk: {} != {}'.format(data.shape,
                                                                                     update_shape))

        image[name][chunk_start:chunk_end] = data


def get_dataset_shape(filename: str, image_id: int, name: str) -> Tuple[int]:
    """Get dataset shape from CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name

    Return:
    shape -- tuple with dataset shape
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        return image[name].shape


def get_dataset_dtype(filename: str, image_id: int, name: str) -> type:
    """Get dataset shape from CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name

    Return:
    type -- array data type
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        return image[name].dtype


def get_dataset_chunks(filename: str, image_id: int, name: str) -> Tuple[int, ...]:
    """Get chunks option for dataset in CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name

    Return:
    chunks -- dataset chunks
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        return image[name].chunks


def get_dataset_compression(filename: str, image_id: int, name: str) -> str:
    """Get chunks option for dataset in CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name

    Return:
    compression -- dataset compression
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        return image[name].compression


def compute_dataset_sum(filename: str, image_id: int, name: str,
                        axis: Union[Tuple[int], int, None] = None,
                        chunk_size: int = 100) -> np.ndarray:
    """Get sum of dataset from CXI file

    Keyword arguments:
    filename -- name of file
    image_id -- id of image group
    name -- dataset name
    axis -- axis to compute sum
    chunk_size -- number of frames in one chunk

    Return:
    result -- array with computed sum
    """

    if not os.path.exists(filename):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

    with h5py.File(filename, 'r') as h5file:
        image = h5file['entry_1/image_{}'.format(image_id)]

        if name not in image:
            raise ValueError('Dataset {} does not exists in image {}'.format(name, image_id))

        sum_stack = []
        num_frames = image[name].shape[0]
        for start in range(0, num_frames, chunk_size):
            end = min(start+chunk_size, num_frames)

            sum_stack.append(np.sum(image[name][start:end], axis=axis))

        return np.stack(sum_stack).sum(axis=0)
