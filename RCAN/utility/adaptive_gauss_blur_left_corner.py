import diplib as dip
import numpy as np
import os
import random


def process_images(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.bmp')):
            # Full path to the image
            input_path = os.path.join(input_folder, filename)

            # Read the image
            img = dip.ImageRead(input_path)

            # Get the size of the image
            width, height = img.Size(0), img.Size(1)

            # Generate random center for blurring
            center_x, center_y = width / 2 , height /2

            # Manually create coordinates for custom center
            y, x = np.indices((height, width))


            # Calculate radius and angle
            radius = np.sqrt(x ** 2 + y ** 2) / 300
            angle = np.arctan2(y, x)

            # Convert to DIPlib images
            radius_image = dip.Image(radius.astype(np.float32))
            angle_image = dip.Image(angle.astype(np.float32))

            # Apply the Adaptive Gaussian blur
            out = dip.AdaptiveGauss(img, [angle_image, radius_image], [1, 5])

            # Define the output path
            output_path = os.path.join(output_folder, filename)

            # Save the output image
            dip.ImageWrite(out, output_path)
            print(f"Processed and saved: {output_path}")


# Define input and output directories
input_dir = '/home/linuxu/Projects/RCAN/RealSR_V3/RealSR_V3_test_HR'
output_dir = '/home/linuxu/Projects/RCAN/RealSR_V3/RealSR_V3_test_HR_blur_center'

# Process all images
process_images(input_dir, output_dir)
