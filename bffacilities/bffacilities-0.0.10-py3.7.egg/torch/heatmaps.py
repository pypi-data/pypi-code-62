import numpy as np

class HeatmapGeneratorWithoutBatch():
    """
    Arguments: 
        out_size(int): image output resolution
        out_channels(int): model output Tensor channels
    """
    def __init__(self, out_size, out_channels):
        self.out_size = out_size
        self.out_channels = out_channels
        sigma = self.out_size / 64
        self.sigma = sigma
        size = 6 * sigma + 3
        x = np.arange(0, size, 1, float)
        y = x[:, np.newaxis]
        x0, y0 = 3*sigma + 1, 3*sigma + 1
        self.g = np.exp(- ((x - x0) ** 2 + (y - y0) ** 2) / (2 * sigma ** 2))

    def __call__(self, keypoints, ratio = 1.0):
        """
        Arguments:
            keypoints: [Tensor(K, 3)] shape: N K 3
            ratio (float): generate target keypoints to dest size heatmap
        """
        batch_size = len(keypoints)
        hms = np.zeros(shape = (batch_size, self.out_size, self.out_size), dtype = np.float32)
        sigma = self.sigma
        # print("KP: ", keypoints)
        for batch_idx, kp in enumerate(keypoints): # batch kps
            # print("KP", kp)
            # assert len(kp) == 4
            for pt in kp:
                # kp torch.Tensor, size (3, )
                # print(idx, pt)
                if pt[2] > 0: 
                    x, y = int(pt[0] * ratio), int(pt[1] * ratio)
                    if x<0 or y<0 or x>=self.out_size or y>=self.out_size:
                        continue
                    ul = int(x - 3*sigma - 1), int(y - 3*sigma - 1)
                    br = int(x + 3*sigma + 2), int(y + 3*sigma + 2)

                    c,d = max(0, -ul[0]), min(br[0], self.out_size) - ul[0]
                    a,b = max(0, -ul[1]), min(br[1], self.out_size) - ul[1]

                    cc,dd = max(0, ul[0]), min(br[0], self.out_size)
                    aa,bb = max(0, ul[1]), min(br[1], self.out_size)
                    hms[batch_idx, aa:bb, cc:dd] = np.maximum(hms[batch_idx, aa:bb,cc:dd], self.g[a:b,c:d])
        return hms
## for debug
# from .torchutils import PlotHelper
# ph = PlotHelper()

class HeatmapGenerator():
    """Generate Heatmap with Batch

    Arguments: 
        out_size(int): image output resolution
        out_channels(int): model output Tensor channels
        sigma(float)
    """
    def __init__(self, out_size, out_channels, sigma = None):
        self.out_size = out_size
        self.out_channels = out_channels
        if sigma is None:
            sigma = self.out_size / 64
        self.sigma = sigma
        size = 6*sigma + 3
        x = np.arange(0, size, 1, float)
        y = x[:, np.newaxis]
        x0, y0 = 3*sigma + 1, 3*sigma + 1
        self.g = np.exp(- ((x - x0) ** 2 + (y - y0) ** 2) / (2 * sigma ** 2))

    def __call__(self, keypoints, ratio = 1.0):
        """
        keypoints: target ground truth keypoints [Tensor(K, 3)] shape: N K 3
        """
        batch_size = len(keypoints)
        hms = np.zeros(shape = (batch_size, self.out_channels, self.out_size, self.out_size), dtype = np.float32)
        sigma = self.sigma
        # print("KP: ", keypoints)
        for batch_idx, kp in enumerate(keypoints): # batch kps
            for idx, pt in enumerate(kp):
                # pt.shape (3,) it is [x, y, v]
                if pt[2] == 0: continue

                x, y = int(pt[0] * ratio), int(pt[1] * ratio)
                if x<0 or y<0 or x>=self.out_size or y>=self.out_size:
                    continue
                ul = int(x - 3*sigma - 1), int(y - 3*sigma - 1)
                br = int(x + 3*sigma + 2), int(y + 3*sigma + 2)

                c,d = max(0, -ul[0]), min(br[0], self.out_size) - ul[0]
                a,b = max(0, -ul[1]), min(br[1], self.out_size) - ul[1]

                cc,dd = max(0, ul[0]), min(br[0], self.out_size)
                aa,bb = max(0, ul[1]), min(br[1], self.out_size)
                # print("HM: ", aa, bb, cc, dd)
                # ph.plotArray(hms[batch_idx, idx, :, :])
                hms[batch_idx, idx, aa:bb,cc:dd] = np.maximum(hms[batch_idx, idx, aa:bb,cc:dd], self.g[a:b,c:d])
                # ph.plotArray(hms[batch_idx, idx, :, :])
        return hms

import torch
from PIL import Image
from torchvision.models.detection.roi_heads import keypoints_to_heatmap
import torchvision
## for debug
# from .torchutils import PlotHelper
# ph = PlotHelper()

def translateKP(targets):
    """
        targets (list(dict))
            dict {
                "boxes": ,
                "keypoints",
            }
    """
    keypoints = []
    for gt in targets: # batch
        tmpkp = []
        for kps in gt["keypoints"]: # N points
            for kp in kps:
            # for this model we have to split all 4 keypoints separately
                tmpkp.append(kp.unsqueeze(0))
        
        # print("Tmpkp: ", tmpkp[0].shape)
        tmpkp = torch.cat(tmpkp, dim=0)
        # print("Tmpkp: ", tmpkp.shape)
        keypoints.append(tmpkp)
    # list()
    return keypoints

def heatmaps_to_keypoints(heatmaps, rois):
    """Extract predicted keypoint locations from heatmaps. Output has shape
    (#rois, 4, #keypoints) with the 4 rows corresponding to (x, y, logit, prob)
    for each keypoint.
    """
    # This function converts a discrete image coordinate in a HEATMAP_SIZE x
    # HEATMAP_SIZE image to a continuous keypoint coordinate. We maintain
    # consistency with keypoints_to_heatmap_labels by using the conversion from
    # Heckbert 1990: c = d + 0.5, where d is a discrete coordinate and c is a
    # continuous coordinate.
    offset_x = rois[:, 0]
    offset_y = rois[:, 1]

    widths = rois[:, 2] - rois[:, 0]
    heights = rois[:, 3] - rois[:, 1]
    widths = widths.clamp(min=1)
    heights = heights.clamp(min=1)
    widths_ceil = widths.ceil()
    heights_ceil = heights.ceil()
    # print("WH: ", widths, heights, widths_ceil, heights_ceil)

    num_keypoints = heatmaps.shape[1]

    if torchvision._is_tracing():
        xy_preds, end_scores = _onnx_heatmaps_to_keypoints_loop(heatmaps, rois,
                                                                widths_ceil, heights_ceil, widths, heights,
                                                                offset_x, offset_y,
                                                                torch.scalar_tensor(num_keypoints, dtype=torch.int64))
        return xy_preds.permute(0, 2, 1), end_scores

    xy_preds = torch.zeros((len(rois), 3, num_keypoints), dtype=torch.float32, device=heatmaps.device)
    end_scores = torch.zeros((len(rois), num_keypoints), dtype=torch.float32, device=heatmaps.device)

    for i in range(len(rois)):
        roi_map_width = int(widths_ceil[i].item())
        roi_map_height = int(heights_ceil[i].item())
        width_correction = widths[i] / roi_map_width
        height_correction = heights[i] / roi_map_height
        roi_map = torch.nn.functional.interpolate(
            heatmaps[i][None], size=(roi_map_height, roi_map_width), mode='bicubic', align_corners=False)[0]
        # roi_map_probs = scores_to_probs(roi_map.copy())
        ## roi_map.shape K, H, W
        w = roi_map.shape[2] ## equals to roi_map_width
        pos = roi_map.reshape(num_keypoints, -1).argmax(dim=1)

        x_int = pos % w
        y_int = (pos - x_int) // w
        # print("ROI HM to KP", x_int, y_int, w, roi_map_height)
        # print(width_correction, height_correction)

        # assert (roi_map_probs[k, y_int, x_int] ==
        #         roi_map_probs[k, :, :].max())
        x = (x_int.float() + 0.5) * width_correction
        y = (y_int.float() + 0.5) * height_correction
        xy_preds[i, 0, :] = x + offset_x[i]
        xy_preds[i, 1, :] = y + offset_y[i]
        xy_preds[i, 2, :] = 1
        end_scores[i, :] = roi_map[torch.arange(num_keypoints), y_int, x_int]

    return xy_preds.permute(0, 2, 1), end_scores

class HeatmapLoss(torch.nn.Module):
    """
    Arguments:
        nstack(int)
        heatmapGenerator(nn.Module)

    loss for detection heatmap
    
    It's calcuates L2 distance between prediction and groundtruth
    """
    def __init__(self, nstack, heatmapGenerator, dest_size=64, cross_entropy=False):
        super().__init__()
        # self.nstack = nstack
        self.generateHm = heatmapGenerator
        self.dest_size = dest_size
        self.cross_entropy = cross_entropy

    def _forward(self, pred, gt):
        # l shape: B C H W
        # print("Loss: ", pred.shape, gt.shape) # B 4 64 64
        l = torch.sqrt((pred - gt)**2)
        # l = l.mean(dim=3).mean(dim=2).mean(dim=1)
        l = l.mean(dim=3).mean(dim=2).sum(dim=1)           
        return l ## l of dim bsize


    def forward(self, combined_hm_preds, targets, image_sizes):
        """Assume that all input image size is equal in width and height

        Arguments:
            combined_hm_preds (list(torch.Tensor)) Stack list[N C H W]
            targets (list(dict))
            image_sizes (list(torch.Tensor))
            # keypoints(list(3d array))  Tensor.size(N, K, 3)
        """
        # print(combined_hm_preds.device, keypoints.device)
        S = len(combined_hm_preds)
        N, K, H, W = combined_hm_preds[0].shape
        device = combined_hm_preds[0].device
        imsize = image_sizes[0][0] # 512
        ratio = self.dest_size / imsize

        combined_loss = []
        if self.cross_entropy:
            keypoints = [target["keypoints"] for target in targets]
            # print(len(keypoints), keypoints[0].shape)
            # keypoints = torch.as_tensor(keypoints)
            heatmaps = []
            roi = torch.as_tensor([[0., 0., 64., 64.]]).to(device)
            for kps in keypoints:
                heatmaps_per_image, valid_per_image = keypoints_to_heatmap(kps, roi, imsize)
                heatmaps.append(heatmaps_per_image.view(-1))

            keypoint_targets = torch.cat(heatmaps, dim=0)
            # keypoint_targets = torch.cat(hms, dim=0)
            # print(keypoint_targets.shape)
            for i in range(S):
                pred = combined_hm_preds[i] # B C H W
                # print(pred.shape, N * K, H * W)
                # print("pred", pred.shape, S)
                # print(pred.shape, hms.shape)
                keypoint_logits = pred.view(N * K, H * W)
                hmloss = F.cross_entropy(keypoint_logits, keypoint_targets)
                combined_loss.append(hmloss)
            combined_loss = torch.stack(combined_loss, dim=0) # .squeeze(0)
        else:
            keypoints = translateKP(targets)

            hms = self.generateHm(keypoints, ratio) # B C H W
            # ph.plotHeatmap(hms)
            hms = torch.as_tensor(hms)
            # ph.plotTensor(hms)
            hms = hms.to(device) # B C H W
            for i in range(S-1, -1, -1):
                pred = combined_hm_preds[i] # B C H W
                hmloss = self._forward(pred, hms)
                combined_loss.append(hmloss)
            # raise ValueError("Test")
            combined_loss = torch.stack(combined_loss, dim=1) # .squeeze(0)
        return combined_loss.mean()

import torch
import torch.nn as nn
from torch.nn import functional as F
import numpy as np
from easydict import EasyDict as edict


def weighted_mse_loss(input, target, weights, size_average):
    out = (input - target) ** 2
    out = out * weights
    if size_average:
        return out.sum() / len(input)
    else:
        return out.sum()

def weighted_l1_loss(input, target, weights, size_average):
    out = torch.abs(input - target)
    out = out * weights
    if size_average:
        return out.sum() / len(input)
    else:
        return out.sum()

def generate_3d_integral_preds_tensor(heatmaps, num_joints, x_dim, y_dim, z_dim):
    assert isinstance(heatmaps, torch.Tensor)

    heatmaps = heatmaps.reshape((heatmaps.shape[0], num_joints, z_dim, y_dim, x_dim))

    accu_x = heatmaps.sum(dim=2)
    accu_x = accu_x.sum(dim=2)
    accu_y = heatmaps.sum(dim=2)
    accu_y = accu_y.sum(dim=3)
    accu_z = heatmaps.sum(dim=3)
    accu_z = accu_z.sum(dim=3)

    accu_x = accu_x * torch.cuda.comm.broadcast(torch.arange(x_dim).type(torch.cuda.FloatTensor), devices=[accu_x.device.index])[0]
    accu_y = accu_y * torch.cuda.comm.broadcast(torch.arange(y_dim).type(torch.cuda.FloatTensor), devices=[accu_y.device.index])[0]
    accu_z = accu_z * torch.cuda.comm.broadcast(torch.arange(z_dim).type(torch.cuda.FloatTensor), devices=[accu_z.device.index])[0]

    accu_x = accu_x.sum(dim=2, keepdim=True)
    accu_y = accu_y.sum(dim=2, keepdim=True)
    accu_z = accu_z.sum(dim=2, keepdim=True)

    return accu_x, accu_y, accu_z


def softmax_integral_tensor(preds, num_joints, output_3d, hm_width, hm_height, hm_depth):
    # global soft max , batch stacks
    preds = preds.reshape((preds.shape[0], num_joints, -1))
    preds = F.softmax(preds, 2)

    # integrate heatmap into joint location
    if output_3d:
        x, y, z = generate_3d_integral_preds_tensor(preds, num_joints, hm_width, hm_height, hm_depth)
    else:
        assert 0, 'Not Implemented!' #TODO: Not Implemented
    x = x / float(hm_width) - 0.5
    y = y / float(hm_height) - 0.5
    z = z / float(hm_depth) - 0.5
    preds = torch.cat((x, y, z), dim=2)
    preds = preds.reshape((preds.shape[0], num_joints * 3))
    return preds

# define loss
def _assert_no_grad(tensor):
    assert not tensor.requires_grad, \
        "nn criterions don't compute the gradient w.r.t. targets - please " \
        "mark these tensors as not requiring gradients"


class L2JointLocationLoss(nn.Module):
    def __init__(self, output_3d, size_average=True, reduce=True):
        super(L2JointLocationLoss, self).__init__()
        self.size_average = size_average
        self.reduce = reduce
        self.output_3d = output_3d

    def forward(self, preds, *args):
        gt_joints = args[0]
        gt_joints_vis = args[1]

        num_joints = int(gt_joints_vis.shape[1] / 3)
        hm_width = preds.shape[-1]
        hm_height = preds.shape[-2]
        hm_depth = preds.shape[-3] // num_joints if self.output_3d else 1

        pred_jts = softmax_integral_tensor(preds, num_joints, self.output_3d, hm_width, hm_height, hm_depth)

        _assert_no_grad(gt_joints)
        _assert_no_grad(gt_joints_vis)
        return weighted_mse_loss(pred_jts, gt_joints, gt_joints_vis, self.size_average)


class L1JointLocationLoss(nn.Module):
    def __init__(self, output_3d, size_average=True, reduce=True):
        super(L1JointLocationLoss, self).__init__()
        self.size_average = size_average
        self.reduce = reduce
        self.output_3d = output_3d

    def forward(self, preds, *args):
        gt_joints = args[0]
        gt_joints_vis = args[1]

        num_joints = int(gt_joints_vis.shape[1] / 3)
        hm_width = preds.shape[-1]
        hm_height = preds.shape[-2]
        hm_depth = preds.shape[-3] // num_joints if self.output_3d else 1

        pred_jts = softmax_integral_tensor(preds, num_joints, self.output_3d, hm_width, hm_height, hm_depth)

        _assert_no_grad(gt_joints)
        _assert_no_grad(gt_joints_vis)
        return weighted_l1_loss(pred_jts, gt_joints, gt_joints_vis, self.size_average)


def get_loss_func(config):
    if config.loss_type == 'L1':
        return L1JointLocationLoss(config.output_3d)
    elif config.loss_type == 'L2':
        return L2JointLocationLoss(config.output_3d)
    else:
        assert 0, 'Error. Unknown heatmap type {}'.format(config.heatmap_type)


# define loss


# define label
def generate_joint_location_label(config, patch_width, patch_height, joints, joints_vis):
    joints[:, 0] = joints[:, 0] / patch_width - 0.5
    joints[:, 1] = joints[:, 1] / patch_height - 0.5
    joints[:, 2] = joints[:, 2] / patch_width

    joints = joints.reshape((-1))
    joints_vis = joints_vis.reshape((-1))
    return joints, joints_vis


def get_label_func(config):
    return generate_joint_location_label


# define label


# define result
def get_joint_location_result(config, patch_width, patch_height, preds):
    # TODO: This cause imbalanced GPU useage, implement cpu version
    hm_width = preds.shape[-1]
    hm_height = preds.shape[-2]
    if config.output_3d:
        hm_depth = hm_width
        num_joints = preds.shape[1] // hm_depth
    else:
        hm_depth = 1
        num_joints = preds.shape[1]

    pred_jts = softmax_integral_tensor(preds, num_joints, config.output_3d, hm_width, hm_height, hm_depth)
    coords = pred_jts.detach().cpu().numpy()
    coords = coords.astype(float)
    coords = coords.reshape((coords.shape[0], int(coords.shape[1] / 3), 3))
    # project to original image size
    coords[:, :, 0] = (coords[:, :, 0] + 0.5) * patch_width
    coords[:, :, 1] = (coords[:, :, 1] + 0.5) * patch_height
    coords[:, :, 2] = coords[:, :, 2] * patch_width
    scores = np.ones((coords.shape[0], coords.shape[1], 1), dtype=float)

    # add score to last dimension
    coords = np.concatenate((coords, scores), axis=2)

    return coords


def get_result_func(config):
    return get_joint_location_result


# define result


# define merge
def merge_flip_func(a, b, flip_pair):
    # NOTE: flip test of integral is implemented in net_modules.py
    return a


def get_merge_func(loss_config):
    return merge_flip_func
# define merge
