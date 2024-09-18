import os

# Path to the folder containing the images
folder_path = '/home/linuxu/Projects/RCAN/RealSR_V3/Nikon/Train/HR_NIKON'  # Replace with the path to your folder

# Iterate through the files in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith('.png'):  # Ensure you're only processing .png files
        # Extract the numeric part of the filename
        number_part = int(filename[:-4])  # Get the number from the filename

        # Subtract 6 from the number
        new_number = number_part - 6

        # Format the new filename with leading zeros (4 digits)
        new_filename = f'{new_number:04d}.png'

        # Get the full path for the old and new names
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_file_path, new_file_path)

        print(f'Renamed: {filename} to {new_filename}')