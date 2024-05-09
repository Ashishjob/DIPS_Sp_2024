from dip import *
import math

class Filtering:

    def __init__(self, image, filter_name, filter_size, var = None):
        """initializes the variables of spatial filtering on an input image
        takes as input:
        image: the noisy input image
        filter_name: the name of the filter to use
        filter_size: integer value of the size of the fitler
        
        """
        self.image = image

        if filter_name == 'arithmetic_mean':
            self.filter = self.get_arithmetic_mean
        elif filter_name == 'geometric_mean':
            self.filter = self.get_geometric_mean
        if filter_name == 'local_noise':
            self.filter = self.get_local_noise
        elif filter_name == 'median':
            self.filter = self.get_median
        elif filter_name == 'adaptive_median':
            self.filter = self.get_adaptive_median

        self.filterSize = filter_size
        self.globalVar = var
        
        self.S_max = 15

    def get_arithmetic_mean(self, roi):
        """Computes the arithmetic mean of the input ROI
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the arithmetic mean value of the roi"""
        
        tot = len(roi)
        sum_roi = math.fsum(roi)
        return sum_roi / tot

    def get_geometric_mean(self, roi):
        """Computes the geometric mean for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the geometric mean value of the roi"""
        
        prod = 1
        for i in range(len(roi)):
            prod = prod * roi[i]
        N = len(roi)
        g_mean = prod ** (1/N)
        return g_mean

    def get_local_noise(self, roi):
        """Computes the local noise reduction value
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the local noise reduction value of the roi"""
        
        g_xy = roi[len(roi)//2]
        l_mean = self.get_arithmetic_mean(roi)
        n_var = self.globalVar

        mean = sum(roi) / len(roi)

        sqDiff = [(p - mean) ** 2 for p in roi]

        lVar = sum(sqDiff) / len(sqDiff)

        res = g_xy - (n_var / lVar) * (g_xy - l_mean)
        return res

    def get_median(self, roi):
        """Computes the median for the input roi
        takes as input:
        roi: region of interest (a list/array of intensity values)
        returns the median value of the roi
        Do not use any in-built median function from numpy or other libraries.
        """
        
        sorted_list = sorted(roi)
        length = len(sorted_list)
        center = (length - 1) // 2

        if (length % 2 != 0):
            return sorted_list[center]
        else:
            return (sorted_list[center] + sorted_list[center + 1]) / 2

    def get_adaptive_median(self, roi):
        """Use this function to implement the adaptive median.
        It is left up to the student to define the input to this function and call it as needed. Feel free to create
        additional functions as needed.
        """
        
        max_window_size = self.S_max
        z_min = min(roi)
        z_max = max(roi)
        filterSize = self.filterSize

        while filterSize <= max_window_size:
            z_med = self.get_median(roi)
            A1 = z_med - z_min
            A2 = z_med - z_max

            if A1 > 0 and A2 < 0:
                z_xy = roi[math.ceil(len(roi) / 2)]
                B1 = z_xy - z_min
                B2 = z_xy - z_max

                if B1 > 0 and B2 < 0:
                    return int(z_xy)
                else:
                    return int(z_med)
            else:
                filterSize = filterSize + 2


    def filtering(self):
        """performs filtering on an image containing Gaussian or salt & pepper noise
        returns the denoised image
        ----------------------------------------------------------
        Note: Here when we perform filtering we are not doing convolution.
        For every pixel in the image, we select a neighborhood of values defined by the kernel and apply a mathematical
        operation for all the elements within the kernel. For example, mean, median, etc.

        Steps:
        1. add the necessary zero padding to the noisy image, that way we have sufficient values to perform the operations on the pixels at the image corners. The number of rows and columns of zero padding is defined by the kernel size
        2. Iterate through the image and for every pixel (i,j) gather the neighbors defined by the kernel into a list (or any data structure)
        3. Pass these values to one of the filters that will compute the necessary mathematical operations (mean, median, etc.)
        4. Save the results at (i,j) in the output image.
        5. return the output image

        Note: You can create extra functions as needed. For example, if you feel that it is easier to create a new function for
        the adaptive median filter as it has two stages, you are welcome to do that.
        For the adaptive median filter assume that S_max (maximum allowed size of the window) is 15
        """
        org_image_copy = self.image.copy()
        org_num_rows = len(org_image_copy)
        org_num_cols = len(org_image_copy[0])

        max_win_size = self.S_max
        if self.filter == self.get_adaptive_median:
            padded_val = max_win_size // 2
            padded_sum = padded_val * 2
        else:
            padded_val = self.filterSize // 2
            padded_sum = padded_val * 2
        
        padded_img = zeros((org_num_rows + padded_sum, org_num_cols + padded_sum))
        padded_img[padded_val:-padded_val, padded_val:-padded_val] = org_image_copy
        output_image = zeros((len(padded_img), len(padded_img[0])))

        for i in range(padded_val, org_num_rows + padded_val + 1):
            for j in range(padded_val, org_num_cols + padded_val + 1):
                region = padded_img[i-padded_val:i+padded_val+1, j-padded_val:j+padded_val+1]
                roi = []
                for x in range(len(region)):
                    for y in range(len(region[0])):
                        roi.append(region[x][y])
                output_image[i][j] = self.filter(roi)

        return output_image[padded_val:-padded_val, padded_val:-padded_val]