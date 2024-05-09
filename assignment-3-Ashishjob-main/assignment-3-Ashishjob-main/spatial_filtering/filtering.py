import numpy as np
from dip import *
import math

class Filtering:

    def __init__(self, image):
        self.image = image

    def get_gaussian_filter(self):
        """Initialzes/Computes and returns a 5X5 Gaussian filter"""

        std_dev = 1
        total = 0
        coeff = 1 / (2 * math.pi * std_dev ** 2)
        gaussian_filter = zeros((5, 5))

        for x in range(5):
            for y in range(5):
                gaussian_filter[x, y] = coeff * math.exp(-((x - 2) ** 2 + (y - 2) ** 2) / (2 * std_dev ** 2))
                total += gaussian_filter[x, y]

        gaussian_filter /= total

        return gaussian_filter

    def get_laplacian_filter(self):
        """Initialzes and returns a 3X3 Laplacian filter"""

        laplacian_filter = array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        return laplacian_filter

    def filter(self, filter_name):
        """Perform filtering on the image using the specified filter, and returns a filtered image
            takes as input:
            filter_name: a string, specifying the type of filter to use ["gaussian", laplacian"]
            return type: a 2d numpy array
                """

        processed_image = self.image.copy()

        if filter_name == "laplacian":
            laplacian_filter = self.get_laplacian_filter()

            padded_img = zeros((processed_image.shape[0] + 2, processed_image.shape[1] + 2))
            padded_img[1:-1, 1:-1] = processed_image

            for x in range(padded_img.shape[0] - 2):
                for y in range(padded_img.shape[1] - 2):
                    sum_val = 0
                    for u in range(3):
                        for v in range(3):
                            sum_val += laplacian_filter[u, v] * padded_img[x + u, y + v]

                    if sum_val > 255:
                        processed_image[x, y] = 255
                    elif sum_val < 0:
                        processed_image[x, y] = 0
                    else:
                        processed_image[x, y] = sum_val

        elif filter_name == "gaussian":
            gaussian_filter = self.get_gaussian_filter()
            filter_sum = 0

            for x in range(5):
                for y in range(5):
                    filter_sum += gaussian_filter[x, y]

            padded_img = zeros((processed_image.shape[0] + 4, processed_image.shape[1] + 4))
            padded_img[2:-2, 2:-2] = processed_image

            for x in range(padded_img.shape[0] - 4):
                for y in range(padded_img.shape[1] - 4):
                    sum_val = 0
                    for u in range(5):
                        for v in range(5):
                            sum_val += gaussian_filter[u, v] * padded_img[x + u, y + v]
                    
                    processed_image[x, y] = sum_val / filter_sum

        return processed_image

