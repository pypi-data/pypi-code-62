# -*- coding: utf-8 -*-
"""
    boris.cli
    ~~~~~~~~~

    A simple command line tool to upload your datasets to
    the WhatToLabel platform.

"""

import hydra

from boris.api import upload_embeddings_from_csv
from boris.api import upload_images_from_folder

from boris.cli._helpers import fix_input_path


def _upload_cli(cfg, is_cli_call=True):
    '''Upload your image dataset and/or embeddings to the WhatToLabel platform.

    Args:
        cfg['path_to_folder']: (str)
            Path to folder which holds images to upload
        cfg['path_to_embeddings']: (str)
            Path to csv file which holds embeddings to upload
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants acces to the platform

    '''

    path_to_folder = cfg['path_to_folder']
    if path_to_folder and is_cli_call:
        path_to_folder = fix_input_path(cfg['path_to_folder'])

    path_to_embeddings = cfg['path_to_embeddings']
    if path_to_embeddings and is_cli_call:
        path_to_embeddings = fix_input_path(cfg['path_to_embeddings'])

    dataset_id = cfg['dataset_id']
    token = cfg['token']

    if not token or not dataset_id:
        print('Please specify your access token and dataset id.')
        print('For help, try: boris-upload --help')
        return

    if path_to_folder:
        mode = cfg['upload']
        upload_images_from_folder(path_to_folder, dataset_id, token, mode=mode)

    if path_to_embeddings:
        max_upload = cfg['emb_upload_bsz']
        upload_embeddings_from_csv(
            path_to_embeddings, dataset_id, token, max_upload=max_upload
        )


@hydra.main(config_path='config/config.yaml')
def upload_cli(cfg):
    '''Upload your image dataset and/or embeddings to the WhatToLabel platform.

    Args:
        cfg['path_to_folder']: (str)
            Path to folder which holds images to upload
        cfg['path_to_embeddings']: (str)
            Path to csv file which holds embeddings to upload
        cfg['dataset_id']: (str) Dataset identifier on the platform
        cfg['token']: (str) Token which grants acces to the platform

    '''
    _upload_cli(cfg)


def entry():
    upload_cli()
