import cv2

from flip.transformers.element import Element
from flip.transformers.transformer import Transformer


class CreateBoundingBoxes(Transformer):
    def map(self, element: Element) -> Element:
        assert element, "element cannot be None"

        element.tags = self.create(element)

        return element

    def create(self, element):
        array = []
        for obj in element.objects:
            new_x, new_y, new_w, new_h = self.bounding_box(obj.image)
            data = {"name": obj.name, "pos": {}}
            data["pos"]["x"] = (obj.x or 0) + new_x
            data["pos"]["y"] = (obj.y or 0) + new_y
            data["pos"]["w"] = new_w
            data["pos"]["h"] = new_h

            array.append(data)

        return array

    def bounding_box(self, image):
        """
        Args:
          image: image to process its width and height
        Description:
          This function
        Returns:
        """

        # Canny edge detection - edge gradient
        edged = cv2.Canny(image, 10, 250)

        # Morphological Transformations
        # applying closing function
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        # Finding_contours
        (cnts, _) = cv2.findContours(
            closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        global x, y, w, h
        global new_img

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)

            if w > 50 and h > 50:
                new_img = image[y: y + h, x: x + w]

        return x, y, new_img.shape[1], new_img.shape[0]
