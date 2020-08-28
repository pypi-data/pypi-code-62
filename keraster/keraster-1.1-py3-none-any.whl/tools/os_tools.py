import os
import shutil


def ensure_path_exists(*paths):
    """
    保证文件夹存在，无则创建
    :param paths: 可以传入多个path
    :return:
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def copy_file_to_dir(source_file, dict_dir):
    """
    复制文件到指定目录
    :param source_file: 文件地址(包含文件名)
    :param dict_dir: 目标地址
    :return:
    """
    shutil.copy(source_file, os.path.join(dict_dir, os.path.basename(source_file)))
