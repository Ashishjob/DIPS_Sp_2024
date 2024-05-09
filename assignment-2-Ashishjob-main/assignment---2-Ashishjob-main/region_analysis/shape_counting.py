import dip
import math

class ShapeCounting:
    def __init__(self):
        pass

    def euclidean_distance(self, point_one, point_two):
        return ((point_one[0] - point_two[0])**2+ (point_one[1] - point_two[1])**2)**(1/2) 

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes as input:
        image: binary image
        return: a list/dict of regions
        """

        # Initialize a dictionary to store the regions
        region_dict = {}
        # Get the dimensions of the image
        img_rows, img_cols = dip.shape(image)
        # Initialize a matrix to store the region labels
        Region = dip.zeros((img_rows, img_cols), int)
        # Initialize a counter for the regions
        region_id = 1

        # Define a function to add a pixel to a region
        def add_to_region(r, c):
            if Region[r][c] in region_dict:
                region_dict[Region[r][c]].append((r, c))
            else:
                region_dict.setdefault(Region[r][c], [(r, c)])

        # Iterate over each pixel in the image
        for row in range(img_rows):
            for col in range(img_cols):
                if image[row][col] == 0:
                    continue

                if image[row][col] == 255:
                    # Scan the left and top pixels
                    if image[row][col - 1] == 0 and image[row - 1][col] == 0:
                        Region[row][col] = region_id
                        add_to_region(row, col)
                        region_id += 1
                    elif image[row][col - 1] == 0 and image[row - 1][col] == 255:
                        Region[row][col] = Region[row - 1][col]
                        add_to_region(row, col)
                    elif image[row][col - 1] == 255 and image[row - 1][col] == 0:
                        Region[row][col] = Region[row][col - 1]
                        add_to_region(row, col)
                    elif image[row][col - 1] == 255 and image[row - 1][col] == 255:
                        Region[row][col] = Region[row - 1][col]
                        add_to_region(row, col)

                        if Region[row][col - 1] != Region[row - 1][col]:
                            for point in region_dict[Region[row][col - 1]]:
                                if point not in region_dict[Region[row][col]]:
                                    region_dict[Region[row][col]].append(point)

                            region_dict.pop(Region[row][col - 1])
                            Region[row][col - 1] = Region[row - 1][col]

        # Return the dictionary of regions
        return region_dict

    def identify_shapes(self, region):
        """Compute shape features area and centroid, and shape
        Ignore shapes smaller than 10 pixels in area.
        takes as input
        region: a list/dict of pixels in a region
        returns: shapes, a data structure with centroid, area, and shape (c, s, r, or e) for each region
        c - circle, s - squares, r - rectangle, and e - ellipse
        """

        # Please print your shape statistics to stdout, one line for each shape
        # Region: <region_no>, centroid: <centroid>, area: <shape area>, shape: <shape type>
        # Example: Region: 871, centroid: (969.11, 51.11), area: 707, shape: c

        # Initialize a dictionary to store the shapes
        shape_dict = {
            'square': [],
            'rectangle': [],
            'circle': [],
            'ellipse': []
        }

        # Iterate over each region in the image
        for region_id, pixels in region.items():
            # Ignore small regions
            if len(pixels) < 10:
                continue

            # Sort the pixels in the region by their coordinates
            sorted_pixels = sorted(pixels, key=lambda pixel: (pixel[0], pixel[1]))
            # Initialize a dictionary to store the properties of the shape
            shape_properties = {
                'region_id': region_id,
                'pixels': sorted_pixels,
                'centroid': (0,0),
                'area': 0,
                'shape_type': ""
            }

            # Find the indices of the first and last pixels in the sorted list
            start_index = 0
            end_index = len(sorted_pixels) - 1

            # If the region is not a vertical line
            if sorted_pixels[start_index][1] != sorted_pixels[end_index][1]:

                # Adjust the start and end indices to exclude noise
                for i in range(len(sorted_pixels)):
                    if sorted_pixels[i][0] == sorted_pixels[i + 1][0]:
                        start_index = i
                        break

                for i in range(len(sorted_pixels) - 1, -1, -1):
                    if sorted_pixels[i][0] == sorted_pixels[i - 1][0]:
                        end_index = i
                        break

                # Find the corners of the bounding box of the region
                top_left = sorted_pixels[start_index] 
                bottom_right = sorted_pixels[end_index]
                top_right = (top_left[0], bottom_right[1])
                bottom_left = (bottom_right[0], top_left[1])

                # Calculate the dimensions of the bounding box
                width_top = self.distance(top_left, top_right)
                width_bottom = self.distance(bottom_left, bottom_right)
                height_left = self.distance(bottom_left, top_left)
                height_right = self.distance(bottom_right, top_right)

                # Calculate the centroid of the region
                midpoint_top = ((top_left[0] + top_right[0]) / 2, (top_left[1] + top_right[1]) / 2)
                midpoint_bottom = ((bottom_left[0] + bottom_right[0]) / 2, (bottom_left[1] + bottom_right[1]) / 2)
                centroid = ((midpoint_top[0] + midpoint_bottom[0]) / 2, (midpoint_top[1] + midpoint_bottom[1]) / 2)
                center = (round(centroid[0]), round(centroid[1]))
                shape_properties['centroid'] = centroid

                # Calculate the area and classify the shape
                area = 0
                semi_major_axis = 0
                semi_minor_axis = self.distance(center, midpoint_top)
                for pixel in sorted_pixels:
                    if pixel[0] == center[0] and pixel[1] <= center[1]:
                        semi_major_axis += 1

                if semi_major_axis > width_top and semi_major_axis > width_bottom:
                    area = math.pi * semi_major_axis * semi_minor_axis
                    shape_properties['area'] = area
                    shape_properties['shape_type'] = 'ellipse'
                    shape_dict['ellipse'].append(shape_properties)

                elif width_top == width_bottom == height_left == height_right:
                    area = width_top**2
                    shape_properties['area'] = area
                    shape_properties['shape_type'] = 'square'
                    shape_dict['square'].append(shape_properties)

                elif width_top == width_bottom and height_left == height_right:
                    area = width_top * height_left
                    shape_properties['area'] = area
                    shape_properties['shape_type'] = 'rectangle'
                    shape_dict['rectangle'].append(shape_properties)
            else:
                # If the region is a vertical line, it is a circle
                top_middle = sorted_pixels[start_index] 
                bottom_middle = sorted_pixels[end_index]
                centroid = ((top_middle[0] + bottom_middle[0]) / 2, (top_middle[1] + bottom_middle[1]) / 2)
                radius = self.distance(top_middle, bottom_middle)
                area = 3.14159 * (radius**2)

                shape_properties['centroid'] = centroid
                shape_properties['area'] = area
                shape_properties['shape_type'] = 'circle'
                shape_dict['circle'].append(shape_properties)

            # Print the properties of the shape
            print(f'Region: {shape_properties["region_id"]}, centroid: {shape_properties["centroid"]}, area: {shape_properties["area"]}, shape: {shape_properties["shape_type"]}')

        return shape_dict

    def count_shapes(self, shapes_data):
        """Compute the count of shapes using the shapes data returned from identify shapes function
           takes as input
           shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
           returns: a dictionary with count of each shape
           Example return value: {'circles': 21, 'ellipses': 25, 'rectangles': 31, 'squares': 23}
           """
        count_s = len(shapes_data['s'])
        count_r = len(shapes_data['r'])
        count_c = len(shapes_data['c'])
        count_e = len(shapes_data['e'])

        return {"circles": count_c, "ellipses": count_e, "rectangles": count_r, "squares": count_s}

    def mark_image_regions(self, image, shapes_data):
        """Creates a new image with computed stats for each shape
        Make a copy of the image on which you can write text.
        takes as input
        image: binary image
        shapes_data: a list/dict of regions, with centroid, shape, and area for each shape
        returns: image marked with center and shape_type"""

        annotated_image = image.copy()

        for shape_categories in shapes_data.values():
            for shape_details in shape_categories:
                center_of_mass = shape_details['centroid']
                center_coordinates = (math.floor(center_of_mass[1]), math.floor(center_of_mass[0]))
                shape_type = shape_details['shape']
                dip.putText(img=annotated_image, text=shape_type, org=center_coordinates, fontFace=dip.FONT_HERSHEY_SIMPLEX, fontScale=.8, color=0, lineType=dip.LINE_AA)

        return annotated_image

