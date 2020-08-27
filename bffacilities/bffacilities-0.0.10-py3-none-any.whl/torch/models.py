import torch
import torch.nn as nn
import torch.nn.functional as F   # 神经网络模块中的常用功能 
from torch.jit.annotations import List, Tuple, Dict, Optional
from torch.nn import Parameter
from collections import OrderedDict

class ResidualModule(nn.Module):
    """
    Residual Module whose in_channels(default) is 256, out_channels(default) is 256

    Arguments:
        input(int): in_channels
        batch(bool): whether to deploy batch normlization layer
        stride(int): stride will be applied in the first ConvLayer
    """
    def __init__(self, in_channels=256, out_channels=256, div=2, \
            batch=False, **kwargs
        ):
        super().__init__()
        # self.name = name

        # padding = kwargs.get('padding', 0)
        width = out_channels // div

        if not batch:
            self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1) # conv3
            self.conv4 = nn.Conv2d(out_channels, width, kernel_size=1)
            self.conv5 = nn.Conv2d(width,  width, kernel_size=3, padding=1) # padding with 0, to keep feature map size
            self.conv3 = nn.Conv2d(width, out_channels, kernel_size=1)  ## conv3
        else:
            # conv3
            self.conv1 = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1),
                nn.BatchNorm2d(out_channels)
                )
            self.conv4 = nn.Sequential(
                nn.Conv2d(out_channels, width, kernel_size=1),
                nn.BatchNorm2d(width)
                )
            self.conv5 = nn.Sequential(
                nn.Conv2d(width,  width, kernel_size=3, padding=1),
                nn.BatchNorm2d(width)
                )
            self.conv3 = nn.Sequential(
                nn.Conv2d(width, out_channels, kernel_size=1),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        # print(self.name, x.shape, self.up)
        out1 = self.conv1(x)
        out1 = F.relu(out1)
        out2 = self.conv4(out1)
        out2 = F.relu(out2)
        out2 = self.conv5(out2)
        out2 = F.relu(out2)
        out2 = self.conv3(out2)
        out2 = F.relu(out2)

        out = out1 + out2
        return out

    def __repr__(self):
        return f"Resnet-{self.name}"

class _HourGlassDownUnit(nn.Sequential):

    def __init__(self, in_channels, out_channels, \
        pool_kernel_size, pool_padding, **kwargs
        ):
        super().__init__(
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(pool_kernel_size, stride=2, padding=pool_padding),
        )
class _HourGlassResDownUnit(nn.Sequential):

    def __init__(self, in_channels, out_channels, \
        pool_kernel_size, pool_padding, **kwargs
        ):
        super().__init__(
            ResidualModule(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.MaxPool2d(pool_kernel_size, stride=2, padding=pool_padding),
        )
    
class _HourGlassUpUnit(nn.Sequential):

    def __init__(self, in_channels, out_channels, **kwargs):
        super().__init__(
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.UpsamplingBilinear2d(scale_factor=2),
        )
    
class _HourGlassResUpUnit(nn.Sequential):

    def __init__(self, in_channels, out_channels, **kwargs):
        super().__init__(
            ResidualModule(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1),
            nn.UpsamplingBilinear2d(scale_factor=2),
        )

class HourGlassModule(nn.Module):
    """Used for conv-deconv

    @Notes:
        Input feature map size should be 32x32 (baseUpSize==1) or 64x64 (baseUpSize==2)

    Arguments:
        in_channels: input feature map channels
        out_channels: output feature map channels

    Desc:
        channels will be always the same
    """

    def __init__(self, in_channels, out_channels, mid_channels=0,\
            baseUpSize=1, debug=False, residual=False, **kwargs
        ):
        super().__init__()
        self.debug = debug
        if mid_channels == 0:
            mid_channels = out_channels
        # if in_channels is 256 input feature map size is 32x32 / 64x64
        # half_mid = mid_channels // 2
        half_mid = mid_channels
        block = _HourGlassResDownUnit if residual else _HourGlassDownUnit

        kernel_size = (2, 2)
        padding = 0
        self.up1 = block(in_channels, mid_channels, pool_kernel_size=kernel_size, pool_padding=padding, stride=2, batch=True)
        # 256 x 16 x 16  # 32 x 32
        self.up2 = block(in_channels, mid_channels, pool_kernel_size=kernel_size, pool_padding=padding, stride=2, batch=True)
        
        # 256 x 8 x 8    # 16 x 16     
        self.up3 = block(in_channels, mid_channels, pool_kernel_size=kernel_size, pool_padding=padding, stride=2, batch=True)
        # 256 x 4 x 4    # 8 x 8
        self.up4 = block(in_channels, mid_channels, pool_kernel_size=kernel_size, pool_padding=padding, stride=2, batch=True)
        # 256 x 2 x 2
        ###############################
        # 256 x 2 x2
        block = _HourGlassResUpUnit if residual else _HourGlassUpUnit
        self.down4 = block(mid_channels, mid_channels)
        # 256 x 4 x 4
        self.down3 = block(mid_channels, mid_channels)
        # 256 x 8 x 8
        self.down2 = block(mid_channels, mid_channels)
        # 256 x 16 x 16
        self.down1 = block(mid_channels, out_channels)
        # 256 x 32 x 32


    def forward(self, x):
        # print(x.shape)
        # 64 x 64
        out1 = self.up1(x)
        # 32 x 32
        out2 = self.up2(out1)
        # 16 x 16
        out3 = self.up3(out2)
        # 8 x 8
        out4 = self.up4(out3)
        # 4 x 4

        # print(dout)
        dout4 = F.relu(self.down4(out4))# + out3)  # s3
        dout3 = F.relu(self.down3(dout4) + out2) # s2
        dout2 = F.relu(self.down2(dout3) + out1) # s1
        dout1 = F.relu(self.down1(dout2))
        # C x 32 x 32
        if self.debug:
            return OrderedDict([
                ['0',dout1], 
                ['1', out1], ['2', out2], ['3', out3],
                ['4', out4], ['5', dout4], ['6', dout3], ['7', dout2],
                # ['s3', s3], ['s2', s2], ['s1', s1]
            ])
        return dout1

import torch
import torch.nn as nn
import torch.nn.functional as F

class PrimaryCaps(nn.Module):
    '''
    The `PrimaryCaps` layer consists of 32 capsule units. Each unit takes
    the output of the `Conv1` layer, which is a `[256, 20, 20]` feature
    tensor (omitting `batch_size`), and performs a 2D convolution with 8
    output channels, kernel size 9 and stride 2, thus outputing a [8, 6, 6]
    tensor. In other words, you can see these 32 capsules as 32 paralleled 2D
    convolutional layers. Then we concatenate these 32 capsules' outputs and
    flatten them into a tensor of size `[1152, 8]`, representing 1152 8D
    vectors, and send it to the next layer `DigitCaps`.

    As indicated in Section 4, Page 4 in the paper, *One can see PrimaryCaps
    as a Convolution layer with Eq.1 as its block non-linearity.*, outputs of
    the `PrimaryCaps` layer are squashed before being passed to the next layer.

    Reference: Section 4, Fig. 1
    '''

    def __init__(self, in_resolution=64):
        '''
        We build 8 capsule units in the `PrimaryCaps` layer, each can be
        seen as a 2D convolution layer.
        '''
        super(PrimaryCaps, self).__init__()
        self.resolution1 = in_resolution
        self.resolution2 = self.resolution1 // 2 - 4

        num_caps = 32
        self.resolution3 = (self.resolution2 ** 2) * num_caps

        self.capsules = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(in_channels=256, out_channels=16, kernel_size=5, stride=2),
                nn.Conv2d(in_channels=16, out_channels=8, kernel_size=3, stride=1, padding=1),
                nn.Conv2d(in_channels=8, out_channels=8, kernel_size=3, stride=1, padding=0),
            )
            
            for i in range(num_caps)
        ])

    def forward(self, x):
        '''
        Each capsule outputs a [batch_size, 8, 6, 6] tensor, we need to
        flatten and concatenate them into a [batch_size, 8, 6*6, 32] size
        tensor and flatten and transpose into `u` [batch_size, 1152, 8], 
        where each [batch_size, 1152, 1] size tensor is the `u_i` in Eq.2. 

        #### Dimension transformation in this layer(ignoring `batch_size`):
        [256, 20, 20] --> [8, 6, 6] x 32 capsules --> [1152, 8]

        Note: `u_i` is one [1, 8] in the final [1152, 8] output, thus there are
        1152 `u_i`s.
        '''
        batch_size = x.size(0)

        u = []
        for i in range(32):
            # Input: [batch_size, 256, 20, 20]
            assert x.shape[-2:] == (self.resolution1, self.resolution1), f"{x.shape}, {self.resolution1}"

            u_i = self.capsules[i](x)
            assert u_i.shape[-3:] == (8, self.resolution2, self.resolution2)
            # u_i: [batch_size, 8, 6, 6]
            u_i = u_i.view(batch_size, 8, -1, 1) # 24 
            # u_i: [batch_size, 8, 36] # 576
            u.append(u_i)

        # u: [batch_size, 8, 36, 1] x 32
        u = torch.cat(u, dim=3)
        # u: [batch_size, 8, 36, 32]
        u = u.view(batch_size, 8, -1) # 576 * 32 == 
        # u: [batch_size, 8, 1152]
        u = torch.transpose(u, 1, 2)
        # u: [batch_size, 1152, 8]
        assert u.data.shape[-2:] == (self.resolution3, 8)

        # Squash before output
        u_squashed = self.squash(u)

        return u_squashed

    def squash(self, u):
        '''
        Args:
            `u`: [batch_size, 1152, 8]

        Return:
            `u_squashed`: [batch_size, 1152, 8]

        In CapsNet, we use the squash function after the output of both 
        capsule layers. Squash functions can be seen as activating functions
        like sigmoid, but for capsule layers rather than traditional fully
        connected layers, as they squash vectors instead of scalars.

        v_j = (norm(s_j) ^ 2 / (1 + norm(s_j) ^ 2)) * (s_j / norm(s_j))

        Reference: Eq.1 in Section 2.
        '''
        batch_size = u.size(0)

        # u: [batch_size, 1152, 8]
        square = u ** 2

        # square_sum for u: [batch_size, 1152]
        square_sum = torch.sum(square, dim=2)

        # norm for u: [batch_size, 1152]
        norm = torch.sqrt(square_sum)

        # factor for u: [batch_size, 1152]
        factor = norm ** 2 / (norm * (1 + norm ** 2))

        # u_squashed: [batch_size, 1152, 8]
        u_squashed = factor.unsqueeze(2) * u
        assert u_squashed.shape[-2:] == (self.resolution3, 8)

        return u_squashed


class Decoder(nn.Module):
    '''
    The decoder network consists of 3 fully connected layers. For each
    [10, 16] output, we mask out the incorrect predictions, and send
    the [16,] vector to the decoder network to reconstruct a [784,] size
    image.

    Reference: Section 4.1, Fig. 2
    '''

    def __init__(self, out_resolution, num_classes=10):
        '''
        The decoder network consists of 3 fully connected layers, with
        512, 1024, 784 neurons each.
        '''
        super().__init__()
        self.num_classes = num_classes

        self.fc1 = nn.Linear(16, 512)
        self.fc2 = nn.Linear(512, 1024)
        self.out_resolution = out_resolution // 2
        self.final_resolution = out_resolution ** 2
        self.fc3 = nn.Linear(1024, self.out_resolution ** 2)
        self.up =  nn.UpsamplingBilinear2d(scale_factor=2)

    def forward(self, v, target):
        '''
        Args:
            `v`: [batch_size, 10, 16]
            `target`: [batch_size, 10]

        Return:
            `reconstruction`: [batch_size, 784]

        We send the outputs of the `DigitCaps` layer, which is a
        [batch_size, 10, 16] size tensor into the decoder network, and
        reconstruct a [batch_size, 784] size tensor representing the image.
        '''
        batch_size = target.size(0)

        target = target.type(torch.FloatTensor)
        # mask: [batch_size, 10, 16]
        mask = torch.stack([target for i in range(16)], dim=2)
        assert mask.shape[-2:] == (10, 16)
        if v.device != torch.device("cpu"):
            mask = mask.to(v.device)

        # v: [bath_size, 10, 16]
        v_masked = mask * v
        v_masked = torch.sum(v_masked, dim=1)
        assert v_masked.shape[-1] == 16

        # Forward
        v = F.relu(self.fc1(v_masked))
        v = F.relu(self.fc2(v))
        reconstruction = torch.sigmoid(self.fc3(v))

        # assert reconstruction.shape[-1] == self.out_resolution
        reconstruction = reconstruction.view(batch_size, 1, self.out_resolution, self.out_resolution)
        reconstruction = self.up(reconstruction)
        return reconstruction # .view(batch_size, self.final_resolution)


class DigitCaps(nn.Module):
    '''
    The `DigitCaps` layer consists of 10 16D capsules. Compared to the traditional
    scalar output neurons in fully connected networks(FCN), the `DigitCaps` layer
    can be seen as an FCN with ten 16-dimensional output neurons, which we call
    these neurons "capsules".

    In this layer, we take the input `[1152, 8]` tensor `u` as 1152 [8,] vectors
    `u_i`, each `u_i` is a 8D output of the capsules from `PrimaryCaps` (see Eq.2
    in Section 2, Page 2) and sent to the 10 capsules. For each capsule, the tensor
    is first transformed by `W_ij`s into [1152, 16] size. Then we perform the Dynamic
    Routing algorithm to get the output `v_j` of size [16,]. As there are 10 capsules,
    the final output is [16, 10] size.

    #### Dimension transformation in this layer(ignoring `batch_size`):
    [1152, 8] --> [1152, 16] --> [1, 16] x 10 capsules --> [10, 16] output

    Note that in our codes we have vectorized these computations, so the dimensions
    above are just for understanding, actual dimensions of tensors are different.
    '''

    def __init__(self, routing, in_resolution, num_classes=10):
        '''
        There is only one parameter in this layer, `W` [1, 1152, 10, 16, 8], where
        every [8, 16] is a weight matrix W_ij in Eq.2, that is, there are 11520
        `W_ij`s in total.

        The the coupling coefficients `b` [64, 1152, 10, 1] is a temporary variable which
        does NOT belong to the layer's parameters. In other words, `b` is not updated
        by gradient back-propagations. Instead, we update `b` by Dynamic Routing
        in every forward propagation. See the docstring of `self.forward` for details.
        '''
        super(DigitCaps, self).__init__()
        self.routing = routing
        self.resolution1 = in_resolution
        self.num_classes = num_classes
        self.W = nn.Parameter(torch.randn(1, in_resolution, self.num_classes, 8, 16))

    def forward(self, u):
        '''
        Args:
            `u`: [batch_size, 1152, 8]
        Return:
            `v`: [batch_size, 10, 16]

        In this layer, we vectorize our computations by calling `W` and using
        `torch.matmul()`. Thus the full computaion steps are as follows.
            1. Expand `W` into batches and compute `u_hat` (Eq.2)
            2. Line 2: Initialize `b` into zeros
            3. Line 3: Start Routing for `r` iterations:
                1. Line 4: c = softmax(b)
                2. Line 5: s = sum(c * u_hat)
                3. Line 6: v = squash(s)
                4. Line 7: b += u_hat * v

        The coupling coefficients `b` can be seen as a kind of attention matrix
        in the attentional sequence-to-sequence networks, which is widely used in
        Neural Machine Translation systems. For tutorials on  attentional seq2seq
        models, see https://arxiv.org/abs/1703.01619 or
        http://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html

        Reference: Section 2, Procedure 1
        '''
        batch_size = u.size(0)

        # First, we need to expand the dimensions of `W` and `u` to compute `u_hat`
        assert u.shape[-2:] == (self.resolution1, 8)
        # u: [batch_size, 1152, 1, 1, 8]
        u = torch.unsqueeze(u, dim=2)
        u = torch.unsqueeze(u, dim=2)
        # Now we compute u_hat in Eq.2
        # u_hat: [batch_size, 1152, 10, 16]
        u_hat = torch.matmul(u, self.W).squeeze()

        # Line 2: Initialize b into zeros
        # b: [batch_size, 1152, 10, 1]
        b = torch.zeros(batch_size, self.resolution1, self.num_classes, 1)
        if b.device != u.device:
            b = b.to(u.device)

        # Start Routing
        for r in range(self.routing):
            # Line 4: c_i = softmax(b_i)
            # c: [b, 1152, 10, 1]
            c = F.softmax(b, dim=2)
            assert c.shape[-3:] == (self.resolution1, self.num_classes, 1)

            # Line 5: s_j = sum_i(c_ij * u_hat_j|i)
            # u_hat: [batch_size, 1152, 10, 16]
            # s: [batch_size, 10, 16]
            s = torch.sum(u_hat * c, dim=1)

            # Line 6: v_j = squash(s_j)
            # v: [batch_size, 10, 16]
            v = self.squash(s)
            assert v.shape[-2:] == ( self.num_classes, 16)

            # Line 7: b_ij += u_hat * v_j
            # u_hat: [batch_size, 1152, 10, 16]
            # v: [batch_size, 10, 16]
            # a: [batch_size, 10, 1152, 16]
            a = u_hat * v.unsqueeze(1)
            # b: [batch_size, 1152, 10, 1]
            b = b + torch.sum(a, dim=3, keepdim=True)

        return v

    def squash(self, s):
        '''
        Args:
            `s`: [batch_size, 10, 16]

        v_j = (norm(s_j) ^ 2 / (1 + norm(s_j) ^ 2)) * (s_j / norm(s_j))

        Reference: Eq.1 in Section 2.
        '''
        batch_size = s.size(0)

        # s: [batch_size, 10, 16]
        square = s ** 2

        # square_sum for v: [batch_size, 10]
        square_sum = torch.sum(square, dim=2)

        # norm for v: [batch_size, 10]
        norm = torch.sqrt(square_sum)

        # factor for v: [batch_size, 10]
        factor = norm ** 2 / (norm * (1 + norm ** 2))

        # v: [batch_size, 10, 16]
        v = factor.unsqueeze(2) * s
        assert v.shape[-2:] == (10, 16)

        return v


class CapsNet(nn.Module):

    def __init__(self, routing, num_classes = 10, **kwargs):
        '''
        The CapsNet consists of 3 layers: `Conv1`, `PrimaryCaps`, `DigitCaps`.`Conv1`
        is an ordinary 2D convolutional layer with 9x9 kernels, stride 2, 256 output
        channels, and ReLU activations. `PrimaryCaps` and `DigitCaps` are two capsule
        layers with Dynamic Routing between them. For further details of these two
        layers, see the docstrings of their classes. For each [1, 28, 28] input image,
        CapsNet outputs a [16, 10] tensor, representing the 16-dimensional output
        vector from 10 digit capsules.

        Reference: Section 4, Figure 1
        '''
        super().__init__()

        self.resolution1 = 28
        self.reconstruct_factor = 0.0005
        self.num_classes = num_classes
        # self.premodel =  nn.Sequential(
        #     nn.Conv2d(in_channels=1, out_channels=8, kernel_size=5, stride=2, padding=2), # 64
        #     nn.Conv2d(in_channels=8, out_channels=8, kernel_size=5, stride=2, padding=2), # 32
        #     nn.Conv2d(in_channels=8, out_channels=1, kernel_size=3, stride=1, padding=0),
        #     nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, stride=1, padding=0)
        # )
        
        self.premodel =  nn.Sequential(
            nn.Conv2d(in_channels=1,  out_channels=8,   kernel_size=5, stride=2, padding=0), # 62
            nn.Conv2d(in_channels=8,  out_channels=16,  kernel_size=3, stride=1, padding=0),  # 60
            nn.Conv2d(in_channels=16, out_channels=32,  kernel_size=5, stride=2, padding=0), # 28
            nn.Conv2d(in_channels=32, out_channels=256, kernel_size=3, stride=1, padding=1), # 28
        )
        # self.Conv1 = nn.Conv2d(in_channels=1, out_channels=256, kernel_size=9) # input_dim - 8
        self.primaryCaps = PrimaryCaps(in_resolution=self.resolution1)
        self.DigitCaps = DigitCaps(routing, self.primaryCaps.resolution3, num_classes=self.num_classes)

        self.Decoder = Decoder(self.resolution1, num_classes=self.num_classes)

    def forward(self, x):
        '''
        Args:
            `x`: [batch_size, 1, 28, 28] MNIST samples
        
        Return:
            `v`: [batch_size, 10, 16] CapsNet outputs, 16D prediction vectors of
                10 digit capsules

        The dimension transformation procedure of an input tensor in each layer:
            0. Input: [batch_size, 1, 28, 28] -->
            1. `Conv1` --> [batch_size, 256, 20, 20] --> 
            2. `PrimaryCaps` --> [batch_size, 8, 6, 6] x 32 capsules --> 
            3. Flatten, concatenate, squash --> [batch_size, 1152, 8] -->
            4. `W_ij`s and `DigitCaps` --> [batch_size, 16, 10] -->
            5. Length of 10 capsules --> [batch_size, 10] output probabilities
        '''
        # Input: [batch_size, 1, 28, 28]
        x = F.relu(self.premodel(x))
        # x = F.relu(self.Conv1(x))
        # PrimaryCaps input: [batch_size, 256, 20, 20]
        u = self.primaryCaps(x)
        # PrimaryCaps output u: [batch_size, 1152, 8] # 18432
        v = self.DigitCaps(u)
        # DigitCaps output v: [batsh_size, 10, 16]
        return v

    def marginal_loss(self, v, target, l=0.5):
        '''
        Args:
            `v`: [batch_size, 10, 16]
            `target`: [batch_size, 10]
            `l`: Scalar, lambda for down-weighing the loss for absent digit classes

        Return:
            `marginal_loss`: Scalar
        
        L_c = T_c * max(0, m_plus - norm(v_c)) ^ 2 + lambda * (1 - T_c) * max(0, norm(v_c) - m_minus) ^2
        
        Reference: Eq.4 in Section 3.
        '''
        batch_size = v.size(0)

        square = v ** 2
        square_sum = torch.sum(square, dim=2)
        # norm: [batch_size, 10]
        norm = torch.sqrt(square_sum)
        assert norm.size() == torch.Size([batch_size, 10])

        # The two T_c in Eq.4
        T_c = target.type(torch.FloatTensor)
        zeros = torch.zeros(norm.size())
        # Use GPU if available
        if v.device != torch.device("cpu"):
            zeros = zeros.to(v.device)
            T_c = T_c.to(v.device)

        # Eq.4
        marginal_loss = T_c * (torch.max(zeros, 0.9 - norm) ** 2) + \
            (1 - T_c) * l * (torch.max(zeros, norm - 0.1) ** 2)
        marginal_loss = torch.sum(marginal_loss)

        return marginal_loss

    def reconstruction_loss(self, reconstruction, image):
        '''
        Args:
            `reconstruction`: [batch_size, 784] Decoder outputs of images
            `image`: [batch_size, 1, 28, 28] MNIST samples

        Return:
            `reconstruction_loss`: Scalar Variable

        The reconstruction loss is measured by a squared differences
        between the reconstruction and the original image. 

        Reference: Section 4.1
        '''
        batch_size = image.size(0)
        # image: [batch_size, 784]
        image = F.interpolate(image, size=self.resolution1) # added by bf.
        # print(image.shape)
        image = image.unsqueeze(1)

        assert image.shape[-2:] == (self.resolution1, self.resolution1), image.shape
        
        # Scalar Variable
        reconstruction_loss = torch.sum((reconstruction - image) ** 2)
        return reconstruction_loss

    def loss(self, v, target, image):
        '''
        Args:
            `v`: [batch_size, 10, 16] CapsNet outputs
            `target`: [batch_size, 10] One-hot MNIST labels
            `image`: [batch_size, 1, 28, 28] MNIST samples

        Return:
            `L`: Scalar Variable, total loss
            `marginal_loss`: Scalar Variable
            `reconstruction_loss`: Scalar Variable

        The reconstruction loss is scaled down by 5e-4, serving as a
        regularization method.

        Reference: Section 4.1
        '''
        batch_size = image.size(0)

        marginal_loss = self.marginal_loss(v, target)

        # Get reconstructions from the decoder network
        reconstruction = self.Decoder(v, target)
        reconstruction_loss = self.reconstruction_loss(reconstruction, image)

        # Scalar Variable
        loss = (marginal_loss + self.reconstruct_factor * reconstruction_loss) / batch_size

        return loss, marginal_loss / batch_size, reconstruction_loss / batch_size
   