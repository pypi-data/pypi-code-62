import torch
from PIL import Image
import numpy as np
class HeatmapLoss(torch.nn.Module):
    """
    Arguments:
        nstack(int)
        heatmapGenerator(nn.Module)

    loss for detection heatmap
    
    It's calcuates L2 distance between prediction and groundtruth
    """
    def __init__(self, nstack, heatmapGenerator, dest_size=64):
        super().__init__()
        self.nstack = nstack
        self.generateHm = heatmapGenerator
        self.dest_size = dest_size

    def _forward(self, pred, gt):
        # l shape: B C H W
        # print("Loss: ", pred.shape, gt.shape) # B 4 64 64
        l = ((pred - gt)**2)
        # l = l.mean(dim=3).mean(dim=2).mean(dim=1)
        l = l.mean(dim=3).mean(dim=2).sum(dim=1)           
        return l ## l of dim bsize

    def forward(self, combined_hm_preds, keypoints, image_sizes):
        """
        Arguments:
            combined_hm_preds (torch.Tensor) B Stack C H W
            keypoints(list(3d array)) 
            image_sizes (list(torch.Tensor))
        """
        # print(combined_hm_preds.device, keypoints.device)
        device = combined_hm_preds.device
        size = self.dest_size / image_sizes[0][0]
        hms = self.generateHm(keypoints, size)
        # for preds, hm in zip(combined_hm_preds, hms):
        #     for h in hm:
                
        #         h *= 255
        #         print("H.shape", h.shape)
        #         h = Image.fromarray(h.astype(np.uint8))
        #         display(h)
        #     preds = preds[0]
        #     for p in preds:
        #         # p = p.unsqueeze(0)
        #         print("P ", p.shape)
        #         p = Image.fromarray(p.mul(255).byte().cpu().numpy())
        #         display(p)
        #     break
        
        hms = torch.as_tensor(hms)
        # areas = torch.as_tensor([t["area"] for t in keypoints])
        hms = hms.to(device)
        combined_loss = []
        for i in range(self.nstack):
            pred = combined_hm_preds[:,i] # B C H W
            combined_loss.append(self._forward(pred, hms))
        combined_loss = torch.stack(combined_loss, dim=1)
        return combined_loss