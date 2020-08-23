from functools import partial
from os import listdir, path

from ject import intersect


def is_file(folder, filename): return path.isfile(path.join(folder, filename))


def get_files(folder, predicate=None, extension=None):
    extension_pred = (lambda f: f.endswith(extension)) if extension else None
    pred = intersect(partial(is_file, folder), predicate, extension_pred)
    return [f for f in listdir(folder) if pred(f)]
