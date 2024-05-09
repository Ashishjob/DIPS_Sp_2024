from .interpolation import interpolation
from dip import *
import math

class Distort:
    def __init__(self):
        pass

    def distortion(self, image, k):
        """Applies distortion to the image
                image: input image
                k: distortion Parameter
                return the distorted image"""
        
        w, h, _ = image.shape
        center_x = w / 2
        center_y = h / 2
        distorted_image = zeros(image.shape, dtype=uint8)

        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                ic = i - center_x
                jc = j - center_y

                r = math.sqrt(ic**2 + jc**2)

                i_cd = ic / (1 + k * r)
                j_cd = jc / (1 + k * r)
                id = round(i_cd + center_x)
                jd = round(j_cd + center_y)
                distorted_image[id][jd] = image[i][j]

        return distorted_image

    def correction_naive(self, distorted_image, k):
        """Applies correction to a distorted image by applying the inverse of the distortion function
        image: the input image
        k: distortion parameter
        return the corrected image"""

        w, h, _ = distorted_image.shape
        center_x = w / 2
        center_y = h / 2

        corrected_image = zeros(distorted_image.shape, dtype=uint8)

        for i in range(distorted_image.shape[0]):
            for j in range(distorted_image.shape[1]):
                ic = i - center_x
                jc = j - center_y

                r = math.sqrt(ic**2 + jc**2)

                i_cd = ic * (1 + k * r)
                j_cd = jc * (1 + k * r)

                id = round(i_cd + center_x)
                jd = round(j_cd + center_y)

                if not (0 <= id < w and 0 <= jd < h):
                    continue

                corrected_image[id][jd] = distorted_image[i][j]

        return corrected_image

    def correction(self, distorted_image, k, interpolation_type):
        """Applies correction to a distorted image and performs interpolation
                image: the input image
                k: distortion parameter
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the corrected image"""

        w, h, _ = distorted_image.shape
        center_x = w / 2
        center_y = h / 2

        corrected_image = zeros(distorted_image.shape, dtype=uint8)

        interpolation_object = interpolation()

        for i in range(w):
            for j in range(h):
                ic = i - center_x
                jc = j - center_y

                r = math.sqrt(ic**2 + jc**2)

                i_cd = ic / (1 + k * r)
                j_cd = jc / (1 + k * r)

                id = i_cd + center_x
                jd = j_cd + center_y

                if interpolation_type == "nearest_neighbor":
                    corrected_image[i][j] = distorted_image[round(id)][round(jd)]
                elif interpolation_type == "bilinear":
                    pt1 = [math.floor(id), math.floor(jd)]
                    pt2 = [math.floor(id), math.ceil(jd)]
                    pt3 = [math.ceil(id), math.floor(jd)]
                    pt4 = [math.ceil(id), math.ceil(jd)]

                    Ipt1 = distorted_image[pt1[0]][pt1[1]]
                    Ipt2 = distorted_image[pt2[0]][pt2[1]]
                    Ipt3 = distorted_image[pt3[0]][pt3[1]]
                    Ipt4 = distorted_image[pt4[0]][pt4[1]]

                    if pt1[1] == pt2[1] or pt3[1] == pt4[1] or pt1[0] == pt3[0]:
                        corrected_image[i][j] = distorted_image[round(id)][round(jd)]
                    else:
                        corrected_image[i][j] = interpolation_object.bilinear_interpolation(
                            pt1, pt2, pt3, pt4, Ipt1, Ipt2, Ipt3, Ipt4, [id, jd]
                        )

        return corrected_image
