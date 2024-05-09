import math
from dip import *
"""
Do not import cv2, numpy and other third party libs
"""


class Operation:

    def __init__(self):
        pass

    def flip(self, image, direction="horizontal"):
        """
          Perform image flipping along horizontal or vertical direction

          image: the input image to flip
          direction: direction along which to flip

          return: output_image
          """

        #Solve The assignment flipping
        
        if (direction == "horizontal"):
            image = image[:, ::-1]
        elif (direction == "vertical"):
            image = image[::-1, :]

        return image

    def chroma_keying(self, foreground, background, target_color, threshold):
        """
        Perform chroma keying to create an image where the targeted green pixels is replaced with
        background

        foreground_img: the input image with green background
        background_img: the input image with normal background
        target_color: the target color to be extracted (green)
        threshold: value to threshold the pixel proximity to the target color

        return: output_image
        """

        # add your code here
        # Please do not change the structure
        # return  foreground # Currently the input image is returned, please replace this with the color extracted image
        
        output_image = foreground.copy()
        for i in range(foreground.shape[0]):
            for j in range(foreground.shape[1]):
                if (math.sqrt((foreground[i][j][0] - target_color[0]) ** 2 + (foreground[i][j][1] - target_color[1]) ** 2 + (foreground[i][j][2] - target_color[2]) ** 2) < threshold):
                    output_image[i][j] = background[i][j]
        return output_image
   