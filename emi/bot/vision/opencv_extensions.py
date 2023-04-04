import cv2
import numpy

from emi.primitives import Rectangle


class OpenCvExtensions:
    @classmethod
    def crop(cls, image: numpy.ndarray, rect: Rectangle) -> numpy.ndarray:
        return image[rect.top : rect.bottom, rect.left : rect.right]

    @classmethod
    def fill_all_contours(cls, mask: numpy.ndarray, contours: list) -> numpy.ndarray:
        white = 255
        cv2.drawContours(mask, contours, -1, white, thickness=-1)
        return mask

    @classmethod
    def extend(cls, image: numpy.ndarray, x: int, y: int) -> numpy.ndarray:
        original_y, original_x = image.shape
        new_shape = (original_y + y, original_x + x)
        new_image = numpy.zeros(new_shape, dtype=numpy.uint8)
        y_start = y // 2
        y_end = y // 2 + original_y
        x_start = x // 2
        x_end = x // 2 + original_x
        new_image[y_start:y_end, x_start:x_end] = image
        return new_image
