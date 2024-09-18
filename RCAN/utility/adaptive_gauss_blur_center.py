import diplib as dip
import os
import numpy as np

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

            # Get image size
            height, width = img.Size(1), img.Size(0)

            # Define the new center for the blur
            center_x, center_y = width // 2, height // 2  # Example center: center of the image

            # Manually create custom radius and angle (phi) coordinates
            y, x = np.indices((height, width))
            x = x - center_x  # Shift origin to center_x
            y = y - center_y  # Shift origin to center_y

            # Calculate radius and angle
            radius = np.sqrt(x ** 2 + y ** 2) / 300
            angle = np.arctan2(y, x)  # Create angle (phi) coordinate

            # Convert to DIPlib images
            radius_image = dip.Image(radius.astype(np.float32))
            angle_image = dip.Image(angle.astype(np.float32))

            # Apply Adaptive Gaussian blur using the computed radius and angle
            out = dip.AdaptiveGauss(img, [angle_image, radius_image], [1, 5])

            # Define the output path
            output_path = os.path.join(output_folder, filename)

            # Save the output image
            dip.ImageWrite(out, output_path)
            print(f"Processed and saved: {output_path}")


# Define input and output directories
input_dir = '/home/linuxu/Projects/RCAN/RCAN_TestCode/HR/Set5/x2'
output_dir = '/home/linuxu/Projects/RCAN/RCAN_TestCode/HR/Set5/x2_blur_center'

# Process all images
process_images(input_dir, output_dir)
