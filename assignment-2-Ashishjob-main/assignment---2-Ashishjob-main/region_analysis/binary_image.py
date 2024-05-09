from dip import *

class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """ Computes the histogram of the input image
        takes as input:
        image: a greyscale image
        returns a histogram as a list """

        # Get the dimensions of the image
        num_rows, num_cols = shape(image)

        # Initialize a histogram with 256 bins (for grayscale values from 0 to 255)
        histogram = [0]*256

        # Iterate over each pixel in the image
        for row in range(num_rows):
            for col in range(num_cols):
                # Increment the histogram bin corresponding to the pixel's grayscale value
                histogram[image[row][col]] += 1

        # Return the histogram
        return histogram

    def find_threshold(self, hist):
        """ analyses a histogram to find the optimal threshold assuming that the input histogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value
        Note: Use the iterative method to calculate the histogram. Do not use the Otsu's method
        Write your code to compute the optimal threshold method.
        This should be implemented using the iterative algorithm discussed in class (See Week 4, Lecture 7, slide 40
        on teams). Do not implement the Otsu's thresholding method. No points are awarded for Otsu's method.
        """

        # Set initial threshold as the middle intensity value
        initial_threshold = len(hist) // 2
        previous_avg_low_intensity = None
        previous_avg_high_intensity = None

        while True:
            avg_low_intensity = 0
            avg_high_intensity = 0
            total_low_intensity_pixels = 0
            total_high_intensity_pixels = 0

            # Calculate the average intensity for pixels below the threshold
            for intensity in range(0, initial_threshold):
                avg_low_intensity += hist[intensity] * intensity
                total_low_intensity_pixels += hist[intensity]

            # Calculate the average intensity for pixels above the threshold
            for intensity in range(initial_threshold, len(hist)):
                avg_high_intensity += hist[intensity] * intensity
                total_high_intensity_pixels += hist[intensity]

            avg_low_intensity /= total_low_intensity_pixels
            avg_high_intensity /= total_high_intensity_pixels
            
            # If the averages have not changed significantly, stop the loop
            if previous_avg_low_intensity and previous_avg_high_intensity and abs(avg_low_intensity - previous_avg_low_intensity) <= 0.0005 and abs(avg_high_intensity - previous_avg_high_intensity) <= 0.0005:
                break

            previous_avg_low_intensity = avg_low_intensity
            previous_avg_high_intensity = avg_high_intensity
            initial_threshold = round((avg_low_intensity + avg_high_intensity) / 2)
            
        # Return the final threshold
        return initial_threshold

    def binarize(self, image, threshold):
        """ Comptues the binary image of the input image based on histogram analysis and thresholding
        takes as input
        image: a greyscale image
        threshold: to binarize the greyscale image
        returns: a binary image """

        # Create a copy of the original image
        thresholded_img = image.copy()

        # Get the dimensions of the image
        num_rows, num_cols = shape(thresholded_img)

        # Iterate over each pixel in the image
        for row in range(num_rows):
            for col in range(num_cols):
                # If the pixel's intensity is less than or equal to the threshold, set it to 0 (black)
                if image[row][col] <= threshold:
                    thresholded_img[row][col] = 0
                # Otherwise, set it to 255 (white)
                else:
                    thresholded_img[row][col] = 255

        # Return the thresholded image
        return thresholded_img


