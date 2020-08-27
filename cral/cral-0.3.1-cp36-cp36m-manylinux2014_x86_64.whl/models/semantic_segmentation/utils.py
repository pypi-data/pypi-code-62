import tensorflow as tf
import numpy as np
from tensorflow.keras.metrics import MeanIoU

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageColor import getrgb

import cv2
# import denseCRF
import pydensecrf.densecrf as dcrf
from pydensecrf.utils import unary_from_labels
# getrgb(color)

STANDARD_COLORS = [
    'black', 'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]

def getbgr(color_name):
    (R,G,B) = getrgb(color_name)
    return (B,G,R)

STANDARD_COLORS_BGR = list(map(getbgr, STANDARD_COLORS))

def annotate_image(image_path, mask_array, ignore_bg=True):
    alpha = 0.5
    assert isinstance(mask_array, np.ndarray)
    mask_array = mask_array.astype(np.uint8)

    H, W = mask_array.shape

    # image_array = cv2.imread(image_path)
    image_array = np.array(Image.open(image_path)).astype(np.uint8)
    image_array = cv2.resize(image_array, (W, H))

    img_color = image_array.copy()
    for i in np.unique(mask_array):
        if ignore_bg and i==0:
            continue
        # if i in id_to_color:
        color_index = i%len(STANDARD_COLORS_BGR)
        img_color[mask_array == i] = STANDARD_COLORS_BGR[color_index]

    cv2.addWeighted(image_array, alpha, img_color, 1 - alpha, 0, img_color)

    # return cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR) 
    return Image.fromarray(img_color) 


# def densecrf(image_array, logits, w1=10.0, alpha=80, beta=13, w2=3.0, gamma=3, it=5.0):
#     """
#     input parameters:
#         I    : a numpy array of shape [H, W, C], where C should be 3.
#                type of I should be np.uint8, and the values are in [0, 255]
#         P    : a probability map of shape [H, W, L], where L is the number of classes
#                type of P should be np.float32
#         param: a tuple giving parameters of CRF (w1, alpha, beta, w2, gamma, it), where
#                 w1    :   weight of bilateral term, e.g. 10.0
#                 alpha :   spatial distance std, e.g., 80
#                 beta  :   rgb value std, e.g., 15
#                 w2    :   weight of spatial term, e.g., 3.0
#                 gamma :   spatial distance std for spatial term, e.g., 3
#                 it    :   iteration number, e.g., 5
#     output parameters:
#         out  : a numpy array of shape [H, W], where pixel values represent class indices. 
#     """
#     param = (w1, alpha, beta, w2, gamma, it)
#     print('trying dcrf ...')
#     print(image_array.dtype, logits.dtype)
#     print(image_array.shape, logits.shape)
#     out = denseCRF.densecrf(image_array.astype(np.uint8), logits.astype(np.float32), param) 
#     return out 

# Fully connected CRF post processing function
def do_crf(im, mask, zero_unsure=True):
    colors, labels = np.unique(mask, return_inverse=True)
    image_size = mask.shape[:2]
    n_labels = len(set(labels.flat))
    d = dcrf.DenseCRF2D(image_size[1], image_size[0], n_labels)  # width, height, nlabels
    try:
        U = unary_from_labels(labels, n_labels, gt_prob=.7, zero_unsure=zero_unsure)
    except ZeroDivisionError:
        print("couldn't perform crf")
        return mask
    d.setUnaryEnergy(U)
    # This adds the color-independent term, features are the locations only.
    d.addPairwiseGaussian(sxy=(3,3), compat=3)
    # This adds the color-dependent term, i.e. features are (x,y,r,g,b).
    # im is an image-array, e.g. im.dtype == np.uint8 and im.shape == (640,480,3)
    d.addPairwiseBilateral(sxy=80, srgb=13, rgbim=im.astype('uint8'), compat=10)
    Q = d.inference(5) # 5 - num of iterations
    MAP = np.argmax(Q, axis=0).reshape(image_size)
    unique_map = np.unique(MAP)
    for u in unique_map: # get original labels back
        np.putmask(MAP, MAP == u, colors[u])
    return MAP
    # MAP = do_crf(frame, labels.astype('int32'), zero_unsure=False)

class SparseMeanIoU(tf.keras.metrics.MeanIoU):
    def __init__(self,
               num_classes=None,
               name='mean_iou',
               dtype=None):
        super(SparseMeanIoU, self).__init__(num_classes = num_classes,name=name, dtype=dtype)
        self.num_classes = num_classes

    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.math.argmax(y_pred, axis=-1)
        return super().update_state(y_true, y_pred, sample_weight)
    def get_config(self):
        config = {'num_classes': self.num_classes}
        base_config = super(SparseMeanIoU, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
    @classmethod
    def from_config(cls, config):
        # Note that while MeanMetricWrapper itself isn't public, objects of this
        # class may be created and added to the model by calling model.compile.
#         fn = config.pop('fn', None)
#         if cls is SparseMeanIoU:
#           return cls(tf.keras.metrics.get(fn), **config)
#         return super(SparseMeanIoU, cls).from_config(config)
        return cls(**config)
