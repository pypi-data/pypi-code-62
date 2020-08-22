#import spot_finder_starfish as sfs
#sfs.find_spots("BigStitcherResults/B3_round1_fused_tp_0_ch_1.tif", "FilteredCompositeImages/B3_round1_fused_tp_0_ch_1.tif")

import imageio
import numpy as np

from starfish.types import Axes, Features
from starfish.core.imagestack.imagestack import ImageStack
from starfish.spots import DecodeSpots, FindSpots

def local_max_peakfinder_test(path, intensity_percentile=99.995, filter_width=2, small_peak_min=4, small_peak_max=100,
               big_peak_min=25, big_peak_max=10000, small_peak_dist=2, big_peak_dist=0.75, block_dim_fraction=0.5,
               spot_pad_pixels=2, keep_existing=False):
    """
    Debugging FindSpots.LocalMaxPeakFinder
    """

    image_stack = imageio.volread(path)
    
    # enhance brightness of spots
    local_max_peakfinder_small = FindSpots.LocalMaxPeakFinder(
        min_distance=small_peak_dist,
        stringency=0,
        min_obj_area=small_peak_min,
        max_obj_area=small_peak_max,
        min_num_spots_detected=2500,
        is_volume=False,
        verbose=False
    )

    images = ImageStack.from_numpy(image_stack[np.newaxis, np.newaxis, :])
    premature_spots = local_max_peakfinder_small.run(images.reduce({Axes.ZPLANE}, func="max"))

if __name__ == "__main__":
    local_max_peakfinder_test("BigStitcherResults/B3_round1_fused_tp_0_ch_1.tif")
