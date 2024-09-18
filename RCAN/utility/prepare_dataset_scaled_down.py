from PIL import Image
import os

# Define the directory with high-resolution images
input_dir = '/home/linuxu/Projects/RCAN/RCAN_TestCode/HR/Set5/x8'
output_dir = '/home/linuxu/Projects/RCAN/RCAN_TestCode/LR/LRBI/Set5/x8'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Define scaling factors
scaling_factors = [2, 3, 4, 8]


# Function to scale images
def scale_image(image, factor):
    width, height = image.size
    new_width = width // factor
    new_height = height // factor
    if not os.path.exists(f'{output_dir}/X{factor}'):
        os.makedirs(f'{output_dir}/X{factor}')
    # return image.resize((new_width, new_height), Image.ANTIALIAS)
    return image.resize((new_width, new_height), Image.Resampling.BICUBIC)



# Process each image in the directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(input_dir, filename)
        image = Image.open(filepath)

        for factor in scaling_factors:
            scaled_image = scale_image(image, factor)
            scaled_filename = f"{os.path.splitext(filename)[0]}x{factor}{os.path.splitext(filename)[1]}"
            scaled_filepath = os.path.join(f'{output_dir}/X{factor}', scaled_filename)
            scaled_image.save(scaled_filepath)
            print(f"Saved {scaled_filepath}")

print("Image scaling completed.")
