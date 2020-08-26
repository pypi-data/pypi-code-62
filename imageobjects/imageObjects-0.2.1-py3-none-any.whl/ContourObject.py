import cv2
import numpy as np


class ContourObject:
    def __init__(self, contour):
        """
        cv2 contours are produced as np.int32 numpy.ndarrays rather than objects that have a set of attributes. Whilst
        this is over kill for simple processes, it can be useful for more complex processes to re-use logic so this
        class constructs an object that contains those processes and attributes

        :param contour: A contour from open cv python
        :type contour: numpy.ndarray
        """
        self.contour = contour

    @property
    def x_list(self):
        """
        All x coordinates from each point in the list of points that made up the contour
        """
        return [x for cord in self.contour for x, _ in cord]

    @property
    def y_list(self):
        """
        All y coordinates from each point in the list of points that made up the contour
        """
        return [y for cord in self.contour for _, y in cord]

    @property
    def min_x(self):
        """
        Min x position found in all coordinates
        """
        return min(self.x_list)

    @property
    def max_x(self):
        """
        Max x position found in all coordinates
        """
        return max(self.x_list)

    @property
    def min_y(self):
        """
        Min y position found in all coordinates
        """
        return min(self.y_list)

    @property
    def max_y(self):
        """
        Max y position found in all coordinates
        """
        return max(self.y_list)

    @property
    def width(self):
        """
        The width of a contour calculated as max X minus min X coordinate position
        """
        return self.max_x - self.min_x

    @property
    def height(self):
        """
        The height of a contour calculated as max X minus min X coordinate position
        """
        return self.max_y - self.min_y

    @property
    def moments(self):
        """
        The cv2 moments of a given contour
        """
        return cv2.moments(self.contour)

    @property
    def area(self):
        """
        The area of a contour
        """
        return cv2.contourArea(self.contour)

    @property
    def gradient(self):
        """
        The gradient of a contour
        """
        return [(self.max_y - self.min_y) / self.max_x - self.min_x]

    @property
    def xy_list(self):
        """
        A list of points in the form of [[x1, y1]...[xN. yN]]
        """
        return [[x, y] for x, y in zip(self.x_list, self.y_list)]

    @property
    def bounding_box_points(self):
        """
        Extract the bounding box from a given contour and then return these points as a list, as well as the min and max
        of the x and y points.

        :return: Bounding box points
        :rtype: list
        """
        x_list = [point[0] for point in cv2.boxPoints(cv2.minAreaRect(self.contour))]
        y_list = [point[1] for point in cv2.boxPoints(cv2.minAreaRect(self.contour))]
        return [[x, y] for x, y in zip(x_list, y_list)]

    @property
    def centroid(self):
        """
        The centroid of the contour in terms of [x, y]
        """
        return [int(self.moments()['m10'] / self.moments()['m00']), int(self.moments()['m01'] / self.moments()['m00'])]

    def scale(self, scale):
        """
        To scale a contour, translate it to the origin by subtracting the centroid and then multiply all positions by a
        scalar. Then just move it back to its original position by adding the distance that was taken away. This is then
        returned as a standard np.int32

        :param scale: float scalar to multiplier the contour by
        :type scale: float

        :return: A scaled contour
        :rtype :numpy.ndarray
        """
        return (((self.contour - self.centroid) * scale).astype(np.int32) + self.centroid).astype(np.int32)

    def draw_contour(self, image, bgr_colour=(180, 180, 180)):
        """
        Draw the current contour on an image
        """
        cv2.drawContours(image, [self.contour], 0, bgr_colour, -1)
