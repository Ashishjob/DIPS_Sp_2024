from dip import *

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        # Get the dimensions of the binary image
        num_rows, num_cols = shape(binary_image)
        # Initialize the compressed image list with the first pixel of the binary image
        encoded_image = [binary_image[0][0]]
        # Initialize a variable to keep track of the last pixel in the previous row
        last_pixel_previous_row = None
        # Initialize a counter for the run length
        run_length = 1

        # Iterate over each pixel in the binary image
        for row in range(num_rows):
            for col in range(num_cols):
                # If we're at the first pixel of a new row (except the first row)
                if col == 0 and row != 0:
                    # If the current pixel is different from the last pixel in the previous row
                    if last_pixel_previous_row != binary_image[row][col]:
                        # Append the run length to the compressed image list and reset the counter
                        encoded_image.append(run_length)
                        run_length = 1
                    else:
                        # Otherwise, increment the counter
                        run_length += 1  
                # If we're at the last pixel of a row
                elif col == num_cols - 1:
                    # If we're also at the last row
                    if row == num_rows - 1:
                        # Append the run length to the compressed image list and break the loop
                        encoded_image.append(run_length)
                        break
                    
                    # Update the last pixel in the previous row and continue to the next iteration
                    last_pixel_previous_row = binary_image[row][col]
                    continue
                
                # If the current pixel is the same as the next pixel
                if binary_image[row][col] == binary_image[row][col + 1]:
                    # Increment the counter
                    run_length += 1
                else:
                    # Otherwise, append the run length to the compressed image list and reset the counter
                    encoded_image.append(run_length)
                    run_length = 1

        # Return the compressed image list
        return encoded_image

    def decode_image(self, rle_code, height , width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """

        # Initialize a binary image of zeros with the given height and width
        decoded_image = zeros((height, width), uint8)
        # Initialize the current row and column in the image
        img_row = 0
        img_col = 0
        # Get the first pixel value from the run-length encoded data
        pixel_value = rle_code[0]
        # Determine if the first pixel is white
        is_white = True if pixel_value == 255 else False

        # Iterate over the run-length encoded data, starting from the second element
        for i in range(1, len(rle_code)):
            # For each run length in the data
            for _ in range(rle_code[i]):
                # If the current pixel is white, set the corresponding pixel in the binary image to white
                if is_white:
                    decoded_image[img_row][img_col] = 255

                # Move to the next column in the image
                img_col += 1

                # If we've reached the end of a row in the image
                if img_col == width:
                    # Reset the column to the start and move to the next row
                    img_col = 0
                    img_row += 1

            # Flip the pixel color for the next run length
            is_white = not is_white

        # Return the decoded binary image
        return decoded_image





        




