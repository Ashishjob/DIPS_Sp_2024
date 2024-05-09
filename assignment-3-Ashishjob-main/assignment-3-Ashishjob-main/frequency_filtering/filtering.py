# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv

import numpy as np
from dip import *

class Filtering:

    def __init__(self, image):
        """initializes the variables for frequency filtering on an input image
        takes as input:
        image: the input image
        """
        self.image = image
        self.mask = self.get_mask

    def get_mask(self, shape):
        """Computes a user-defined mask
        takes as input:
        shape: the shape of the mask to be generated
        rtype: a 2d numpy array with size of shape
        """

        mask = np.ones(shape, dtype=np.uint8)

        mask[225:240, 290:305] = 0
        mask[265:275, 275:285] = 0
        mask[275:290, 210:225] = 0
        mask[240:250, 230:240] = 0

        return mask

    def post_process_image(self, image):
        """Post processing to display DFTs and IDFTs
        takes as input:
        image: the image obtained from the inverse fourier transform
        return an image with full contrast stretch
        -----------------------------------------------------
        You can perform post processing as needed. For example,
        1. You can perfrom log compression
        2. You can perfrom a full contrast stretch (fsimage)
        3. You can take negative (255 - fsimage)
        4. etc.
        """

        minv = np.min(image)
        maxv = np.max(image)
        stretched_image = (image - minv) * (255.0 / (maxv - minv))
        stretched_image = np.uint8(stretched_image)

        return stretched_image

    def filter(self):
        """Performs frequency filtering on an input image
        returns a filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering
        ----------------------------------------------------------
        You are allowed to use inbuilt functions to compute fft
        There are packages available in numpy as well as in opencv
        Steps:
        1. Compute the fft of the image
        2. shift the fft to center the low frequencies
        3. get the mask (write your code in functions provided above) the functions can be called by self.filter(shape)
        4. filter the image frequency based on the mask (Convolution theorem)
        5. compute the inverse shift
        6. compute the inverse fourier transform
        7. compute the magnitude
        8. You will need to do post processing on the magnitude and depending on the algorithm (use post_process_image to write this code)
        Note: You do not have to do zero padding as discussed in class, the inbuilt functions takes care of that
        filtered image, magnitude of frequency_filtering, magnitude of filtered frequency_filtering: Make sure all images being returned have grey scale full contrast stretch and dtype=uint8
        """

        fft_image = fft2(self.image)

        fft_image_shifted = fftshift(fft_image)
        mag_image = np.abs(fft_image_shifted)
        log_mag_image = np.log(1 + mag_image).astype(np.uint8)
        new_mag_image = self.post_process_image(log_mag_image)

        mask = self.get_mask(fft_image_shifted.shape)

        fft_image_filtered = fft_image_shifted * mask
        filtered_image_mag = np.abs(fft_image_filtered)
        log_filtered_image_mag = np.log(1 + filtered_image_mag).astype(np.uint8)
        filtered_image = self.post_process_image(log_filtered_image_mag)

        fft_image_inverse_shifted = ifftshift(fft_image_filtered)

        inverse_fft_image = ifft2(fft_image_inverse_shifted)

        inverse_fft_image_mag = np.abs(inverse_fft_image)
        inverse_fft_image_mag = self.post_process_image(inverse_fft_image_mag)

        return [inverse_fft_image_mag, new_mag_image, filtered_image]
