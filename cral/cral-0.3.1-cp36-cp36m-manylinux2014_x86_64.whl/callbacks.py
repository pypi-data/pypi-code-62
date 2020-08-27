import math
import os
import shutil
import tempfile

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard

from cral.tracking import log_artifact
from cral.tracking.utils.autologging_utils import try_mlflow_log


class ModelCheckpointAndUpload(ModelCheckpoint):
    """docstring for ModelCheckpointAndUpload"""
    # def __init__(self, arg):
    #     super(ModelCheckpointAndUpload, self).__init__()
    #     self.arg = arg

    def _save_model(self, epoch, logs):
        super(ModelCheckpointAndUpload, self)._save_model(epoch, logs)
        filepath = self._get_file_path(epoch, logs)

        if os.path.isdir(filepath):
            output_filename = os.path.join(tempfile.gettempdir(),'checkpoint_to_upload_cral') # .zip is automatically postfixed

            if os.path.isfile(output_filename):
                os.remove(output_filename)
            # zip filepath folder
            shutil.make_archive(output_filename, 'zip', filepath)
            # log as artifact
            print(f"Uploading checkpoint {output_filename} ...")
            try_mlflow_log(log_artifact, key=os.path.basename(filepath)+'.zip', path=output_filename+'.zip')

class TensorboardUpload(TensorBoard):
    """docstring for TensorboardUpload"""
    # def __init__(self, arg):
    #     super(TensorboardUpload, self).__init__()
    #     self.arg = arg

    def _log_epoch_metrics(self, epoch, logs):
        super(TensorboardUpload, self)._log_epoch_metrics(epoch, logs)

        train_logs = {k: v for k, v in logs.items() if not k.startswith('val_')}
        val_logs = {k: v for k, v in logs.items() if k.startswith('val_')}

        _log_write_dir = self._get_log_write_dir()

        if train_logs:
            _train_dir = os.path.join( _log_write_dir, 'train')
            output_filename = os.path.join(tempfile.gettempdir(),'tboard_train_to_upload_cral')

            if os.path.isfile(output_filename):
                os.remove(output_filename)
            # zip filepath folder
            shutil.make_archive(output_filename, 'zip', _train_dir)
            # log as artifact
            try_mlflow_log(log_artifact, key='train_tensorboard.zip', path=output_filename+'.zip')

        if val_logs:
            _val_dir = os.path.join( _log_write_dir, 'validation')
            output_filename = os.path.join(tempfile.gettempdir(),'tboard_val_to_upload_cral')

            if os.path.isfile(output_filename):
                os.remove(output_filename)
            # zip filepath folder
            shutil.make_archive(output_filename, 'zip', _val_dir)
            # log as artifact
            try_mlflow_log(log_artifact, key='validation_tensorboard.zip', path=output_filename+'.zip')        


def checkpoint_callback(snapshot_every_epoch, snapshot_path, checkpoint_prefix, save_h5=True):

    assert isinstance(save_h5, bool)

    tf.io.gfile.makedirs(snapshot_path) #, exist_ok=True)

    snapshot_every_epoch = int(snapshot_every_epoch)

    checkpoint_name = os.path.join(snapshot_path, str(checkpoint_prefix)+'_{epoch:02d}')

    if save_h5:
        checkpoint_name += '.h5'
        
    return ModelCheckpointAndUpload(
        checkpoint_name,
        verbose=1,
        period=snapshot_every_epoch)

    # else:
    #     return tf.keras.callbacks.ModelCheckpoint(
    #         os.path.join(snapshot_path, str(checkpoint_prefix)+'_{epoch:02d}'),
    #         verbose=1,
    #         period=snapshot_every_epoch)
