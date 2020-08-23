"""
Adapted from: https://github.com/facebookresearch/moco

Original work is: Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
This implementation is: Copyright (c) PyTorch Lightning, Inc. and its affiliates. All Rights Reserved
"""

from typing import Union

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import torchvision
from torch import nn

from pl_bolts.datamodules import CIFAR10DataModule, STL10DataModule
from pl_bolts.datamodules.ssl_imagenet_datamodule import SSLImagenetDataModule
from pl_bolts.metrics import precision_at_k, mean
from pl_bolts.models.self_supervised.moco.transforms import (
    Moco2TrainCIFAR10Transforms,
    Moco2EvalCIFAR10Transforms,
    Moco2TrainSTL10Transforms,
    Moco2EvalSTL10Transforms,
    Moco2TrainImagenetTransforms,
    Moco2EvalImagenetTransforms
)


class MocoV2(pl.LightningModule):

    def __init__(self,
                 base_encoder: Union[str, torch.nn.Module] = 'resnet18',
                 emb_dim: int = 128,
                 num_negatives: int = 65536,
                 encoder_momentum: float = 0.999,
                 softmax_temperature: float = 0.07,
                 learning_rate: float = 0.03,
                 momentum: float = 0.9,
                 weight_decay: float = 1e-4,
                 datamodule: pl.LightningDataModule = None,
                 data_dir: str = './',
                 batch_size: int = 256,
                 use_mlp: bool = False,
                 num_workers: int = 8,
                 *args, **kwargs):
        """
        PyTorch Lightning implementation of `Moco <https://arxiv.org/abs/2003.04297>`_

        Paper authors: Xinlei Chen, Haoqi Fan, Ross Girshick, Kaiming He.

        Code adapted from `facebookresearch/moco <https://github.com/facebookresearch/moco>`_ to Lightning by:

            - `William Falcon <https://github.com/williamFalcon>`_

        Example:

            >>> from pl_bolts.models.self_supervised import MocoV2
            ...
            >>> model = MocoV2()

        Train::

            trainer = Trainer()
            trainer.fit(model)

        CLI command::

            # cifar10
            python moco2_module.py --gpus 1

            # imagenet
            python moco2_module.py
                --gpus 8
                --dataset imagenet2012
                --data_dir /path/to/imagenet/
                --meta_dir /path/to/folder/with/meta.bin/
                --batch_size 32

        Args:
            base_encoder: torchvision model name or torch.nn.Module
            emb_dim: feature dimension (default: 128)
            num_negatives: queue size; number of negative keys (default: 65536)
            encoder_momentum: moco momentum of updating key encoder (default: 0.999)
            softmax_temperature: softmax temperature (default: 0.07)
            learning_rate: the learning rate
            momentum: optimizer momentum
            weight_decay: optimizer weight decay
            datamodule: the DataModule (train, val, test dataloaders)
            data_dir: the directory to store data
            batch_size: batch size
            use_mlp: add an mlp to the encoders
            num_workers: workers for the loaders
        """

        super().__init__()
        self.save_hyperparameters()

        # use CIFAR-10 by default if no datamodule passed in
        if datamodule is None:
            datamodule = CIFAR10DataModule(data_dir)
            datamodule.train_transforms = Moco2TrainCIFAR10Transforms()
            datamodule.val_transforms = Moco2EvalCIFAR10Transforms()

        self.datamodule = datamodule

        # create the encoders
        # num_classes is the output fc dimension
        self.encoder_q, self.encoder_k = self.init_encoders(base_encoder)

        if use_mlp:  # hack: brute-force replacement
            dim_mlp = self.encoder_q.fc.weight.shape[1]
            self.encoder_q.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.encoder_q.fc)
            self.encoder_k.fc = nn.Sequential(nn.Linear(dim_mlp, dim_mlp), nn.ReLU(), self.encoder_k.fc)

        for param_q, param_k in zip(self.encoder_q.parameters(), self.encoder_k.parameters()):
            param_k.data.copy_(param_q.data)  # initialize
            param_k.requires_grad = False  # not update by gradient

        # create the queue
        self.register_buffer("queue", torch.randn(emb_dim, num_negatives))
        self.queue = nn.functional.normalize(self.queue, dim=0)

        self.register_buffer("queue_ptr", torch.zeros(1, dtype=torch.long))

    def init_encoders(self, base_encoder):
        """
        Override to add your own encoders
        """

        template_model = getattr(torchvision.models, base_encoder)
        encoder_q = template_model(num_classes=self.hparams.emb_dim)
        encoder_k = template_model(num_classes=self.hparams.emb_dim)

        return encoder_q, encoder_k

    @torch.no_grad()
    def _momentum_update_key_encoder(self):
        """
        Momentum update of the key encoder
        """
        for param_q, param_k in zip(self.encoder_q.parameters(), self.encoder_k.parameters()):
            em = self.hparams.encoder_momentum
            param_k.data = param_k.data * em + param_q.data * (1. - em)

    @torch.no_grad()
    def _dequeue_and_enqueue(self, keys):
        # gather keys before updating queue
        if self.use_ddp or self.use_ddp2:
            keys = concat_all_gather(keys)

        batch_size = keys.shape[0]

        ptr = int(self.queue_ptr)
        assert self.hparams.num_negatives % batch_size == 0  # for simplicity

        # replace the keys at ptr (dequeue and enqueue)
        self.queue[:, ptr:ptr + batch_size] = keys.T
        ptr = (ptr + batch_size) % self.hparams.num_negatives  # move pointer

        self.queue_ptr[0] = ptr

    @torch.no_grad()
    def _batch_shuffle_ddp(self, x):  # pragma: no-cover
        """
        Batch shuffle, for making use of BatchNorm.
        *** Only support DistributedDataParallel (DDP) model. ***
        """
        # gather from all gpus
        batch_size_this = x.shape[0]
        x_gather = concat_all_gather(x)
        batch_size_all = x_gather.shape[0]

        num_gpus = batch_size_all // batch_size_this

        # random shuffle index
        idx_shuffle = torch.randperm(batch_size_all).cuda()

        # broadcast to all gpus
        torch.distributed.broadcast(idx_shuffle, src=0)

        # index for restoring
        idx_unshuffle = torch.argsort(idx_shuffle)

        # shuffled index for this gpu
        gpu_idx = torch.distributed.get_rank()
        idx_this = idx_shuffle.view(num_gpus, -1)[gpu_idx]

        return x_gather[idx_this], idx_unshuffle

    @torch.no_grad()
    def _batch_unshuffle_ddp(self, x, idx_unshuffle):  # pragma: no-cover
        """
        Undo batch shuffle.
        *** Only support DistributedDataParallel (DDP) model. ***
        """
        # gather from all gpus
        batch_size_this = x.shape[0]
        x_gather = concat_all_gather(x)
        batch_size_all = x_gather.shape[0]

        num_gpus = batch_size_all // batch_size_this

        # restored index for this gpu
        gpu_idx = torch.distributed.get_rank()
        idx_this = idx_unshuffle.view(num_gpus, -1)[gpu_idx]

        return x_gather[idx_this]

    def forward(self, img_q, img_k):
        """
        Input:
            im_q: a batch of query images
            im_k: a batch of key images
        Output:
            logits, targets
        """

        # compute query features
        q = self.encoder_q(img_q)  # queries: NxC
        q = nn.functional.normalize(q, dim=1)

        # compute key features
        with torch.no_grad():  # no gradient to keys
            self._momentum_update_key_encoder()  # update the key encoder

            # shuffle for making use of BN
            if self.use_ddp or self.use_ddp2:
                img_k, idx_unshuffle = self._batch_shuffle_ddp(img_k)

            k = self.encoder_k(img_k)  # keys: NxC
            k = nn.functional.normalize(k, dim=1)

            # undo shuffle
            if self.use_ddp or self.use_ddp2:
                k = self._batch_unshuffle_ddp(k, idx_unshuffle)

        # compute logits
        # Einstein sum is more intuitive
        # positive logits: Nx1
        l_pos = torch.einsum('nc,nc->n', [q, k]).unsqueeze(-1)
        # negative logits: NxK
        l_neg = torch.einsum('nc,ck->nk', [q, self.queue.clone().detach()])

        # logits: Nx(1+K)
        logits = torch.cat([l_pos, l_neg], dim=1)

        # apply temperature
        logits /= self.hparams.softmax_temperature

        # labels: positive key indicators
        labels = torch.zeros(logits.shape[0], dtype=torch.long)
        labels = labels.type_as(logits)

        # dequeue and enqueue
        self._dequeue_and_enqueue(k)

        return logits, labels

    def training_step(self, batch, batch_idx):
        # in STL10 we pass in both lab+unl for online ft
        if self.hparams.datamodule.name == 'stl10':
            labeled_batch = batch[1]
            unlabeled_batch = batch[0]
            batch = unlabeled_batch

        (img_1, img_2), _ = batch

        output, target = self(img_q=img_1, img_k=img_2)
        loss = F.cross_entropy(output.float(), target.long())

        acc1, acc5 = precision_at_k(output, target, top_k=(1, 5))

        log = {
            'train_loss': loss,
            'train_acc1': acc1,
            'train_acc5': acc5
        }
        return {'loss': loss, 'log': log, 'progress_bar': log}

    def validation_step(self, batch, batch_idx):
        # in STL10 we pass in both lab+unl for online ft
        if self.hparams.datamodule.name == 'stl10':
            labeled_batch = batch[1]
            unlabeled_batch = batch[0]
            batch = unlabeled_batch

        (img_1, img_2), labels = batch

        output, target = self(img_q=img_1, img_k=img_2)
        loss = F.cross_entropy(output, target.long())

        acc1, acc5 = precision_at_k(output, target, top_k=(1, 5))

        results = {
            'val_loss': loss,
            'val_acc1': acc1,
            'val_acc5': acc5
        }
        return results

    def validation_epoch_end(self, outputs):
        val_loss = mean(outputs, 'val_loss')
        val_acc1 = mean(outputs, 'val_acc1')
        val_acc5 = mean(outputs, 'val_acc5')

        log = {
            'val_loss': val_loss,
            'val_acc1': val_acc1,
            'val_acc5': val_acc5
        }
        return {'val_loss': val_loss, 'log': log, 'progress_bar': log}

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), self.hparams.learning_rate,
                                    momentum=self.hparams.momentum,
                                    weight_decay=self.hparams.weight_decay)
        return optimizer

    @staticmethod
    def add_model_specific_args(parent_parser):
        from test_tube import HyperOptArgumentParser
        parser = HyperOptArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--base_encoder', type=str, default='resnet18')
        parser.add_argument('--emb_dim', type=int, default=128)
        parser.add_argument('--num_workers', type=int, default=8)
        parser.add_argument('--num_negatives', type=int, default=65536)
        parser.add_argument('--encoder_momentum', type=float, default=0.999)
        parser.add_argument('--softmax_temperature', type=float, default=0.07)
        parser.add_argument('--learning_rate', type=float, default=0.03)
        parser.add_argument('--momentum', type=float, default=0.9)
        parser.add_argument('--weight_decay', type=float, default=1e-4)
        parser.add_argument('--data_dir', type=str, default='./')
        parser.add_argument('--dataset', type=str, default='cifar10', help='cifar10, stl10, imagenet2012')
        parser.add_argument('--batch_size', type=int, default=256)
        parser.add_argument('--use_mlp', action='store_true')
        parser.add_argument('--meta_dir', default='.', type=str, help='path to meta.bin for imagenet')

        return parser


# utils
@torch.no_grad()
def concat_all_gather(tensor):
    """
    Performs all_gather operation on the provided tensors.
    *** Warning ***: torch.distributed.all_gather has no gradient.
    """
    tensors_gather = [torch.ones_like(tensor)
                      for _ in range(torch.distributed.get_world_size())]
    torch.distributed.all_gather(tensors_gather, tensor, async_op=False)

    output = torch.cat(tensors_gather, dim=0)
    return output


# todo: covert to CLI func and add test
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    # trainer args
    parser = pl.Trainer.add_argparse_args(parser)

    # model args
    parser = MocoV2.add_model_specific_args(parser)
    args = parser.parse_args()

    if args.dataset == 'cifar10':
        datamodule = CIFAR10DataModule.from_argparse_args(args)
        datamodule.train_transforms = Moco2TrainCIFAR10Transforms()
        datamodule.val_transforms = Moco2EvalCIFAR10Transforms()

    elif args.dataset == 'stl10':
        datamodule = STL10DataModule.from_argparse_args(args)
        datamodule.train_dataloader = datamodule.train_dataloader_mixed
        datamodule.val_dataloader = datamodule.val_dataloader_mixed
        datamodule.train_transforms = Moco2TrainSTL10Transforms()
        datamodule.val_transforms = Moco2EvalSTL10Transforms()

    elif args.dataset == 'imagenet2012':
        datamodule = SSLImagenetDataModule.from_argparse_args(args)
        datamodule.train_transforms = Moco2TrainImagenetTransforms()
        datamodule.val_transforms = Moco2EvalImagenetTransforms()

    model = MocoV2(**args.__dict__, datamodule=datamodule)

    trainer = pl.Trainer.from_argparse_args(args)
    trainer.fit(model)
