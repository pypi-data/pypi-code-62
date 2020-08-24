import os
import os.path as path
import sys

from PIL import Image
from ._mscviplib import *


Runner.SetPackageInstallDir(path.dirname(_mscviplib.__file__))

def test():
    from  mscviplib.test.Test_ResizeImage import Test_ResizeImage as Test_ResizeImage
    test = Test_ResizeImage()
    test_result = test.run()

    if len(test_result.failures) < 1:
      print("Passed!!!") 
    else:
      print("FAILED!!!")
      sys.exit(1)
  
def GetImageMetadata(image):
    """Get mscviplib.ImageMetadataByte from a PIL.Image object.

    Args:
        image: PIL image object. 

    Returns:
        ImageMetadataByte object.

    """
    numChannels = len(image.mode)
    image_metadata = ImageMetadataByte()
    image_metadata.Height = image.height
    image_metadata.Width = image.width
    image_metadata.Channels = numChannels
    image_metadata.ColorSpace = ColorSpace.RGB
    image_metadata.Stride = image_metadata.Width * numChannels
    return image_metadata