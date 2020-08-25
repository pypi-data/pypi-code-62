import os
import torch

from hydra import utils


def fix_input_path(path):
    """Fix broken relative paths.

    """
    if not os.path.isabs(path):
        path = utils.to_absolute_path(path)
    return path


def filter_state_dict(state_dict):
    """Prevent unexpected key error when loading PyTorch-Lightning checkpoints
       by removing the unnecessary prefix model. from each key.

    """
    new_state_dict = {}
    for key, item in state_dict.items():
        new_key = '.'.join(key.split('.')[1:])
        new_state_dict[new_key] = item
    return new_state_dict


def _is_url(checkpoint):
    is_url = ('https://storage.googleapis.com' in checkpoint)
    return is_url


def _model_zoo(model):

    zoo = {

        'resnet-9/simclr/d16/w0.0625':
        'https://storage.googleapis.com/models_boris/whattolabel-resnet9-simclr-d16-w0.0625-i-ce0d6bd9.pth',

        'resnet-9/simclr/d16/w0.125':
        'https://storage.googleapis.com/models_boris/whattolabel-resnet9-simclr-d16-w0.125-i-7269c38d.pth',

        'resnet-18/simclr/d16/w1.0':
        'https://storage.googleapis.com/models_boris/whattolabel-resnet18-simclr-d16-w1.0-i-58852cb9.pth',

        'resnet-18/simclr/d32/w1.0':
        'https://storage.googleapis.com/models_boris/whattolabel-resnet18-simclr-d32-w1.0-i-085d0693.pth',

        'resnet-34/simclr/d16/w1.0':
        'https://storage.googleapis.com/models_boris/whattolabel-resnet34-simclr-d16-w1.0-i-6e80d963.pth',

    }

    key = model['name']
    key += '/simclr'
    key += '/d' + str(model['num_ftrs'])
    key += '/w' + str(float(model['width']))

    if key in zoo.keys():
        return zoo[key], key
    else:
        return '', key


def load_state_dict_from_url(url, map_location=None):

    try:
        state_dict = torch.hub.load_state_dict_from_url(
            url, map_location=map_location
        )
        return state_dict
    except Exception:
        print('Not able to load state dict from %s' % (url))
        print('Retrying with http:// prefix')
    try:
        url = url.replace('https', 'http')
        state_dict = torch.hub.load_state_dict_from_url(
            url, map_location=map_location
        )
        return state_dict
    except Exception:
        print('Not able to load state dict from %s' % (url))

    # in this case downloading the pre-trained model was not possible
    # notify the user and return
    return {'state_dict': None}
