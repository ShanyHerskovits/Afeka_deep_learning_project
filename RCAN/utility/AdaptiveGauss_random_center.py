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
            center_x, center_y = random.randint(0, width - 1), random.randint(0, height - 1)

            # Manually create coordinates for custom center
            y, x = np.indices((height, width))
            x = x - center_x
            y = y - center_y

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
input_dir = 'data/RealSR(V3)/Canon/Train/HR_same_image_for_demo'
output_dir = 'data/RealSR(V3)/Canon/Train/HR_same_image_for_demo/HR_same_image_for_demo_blur'

# Process all images
process_images(input_dir, output_dir)
