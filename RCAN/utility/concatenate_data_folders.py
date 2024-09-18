import os
import shutil

# Paths to the folders
folder1_path = '/home/linuxu/Projects/RCAN/RealSR_V3/Test_HR'  # Replace with the path to your first folder
folder2_path = '/home/linuxu/Projects/RCAN/RealSR_V3/HR'  # Replace with the path to your second folder

# Get the last number from folder1
last_number = 50  # Since your last file in folder1 is 0206.png

# Iterate through the files in folder2
for count, filename in enumerate(sorted(os.listdir(folder2_path)), start=1):
    # Create the new name with the correct number
    new_number = last_number + count
    new_filename = f'{new_number:04d}.png'

    # Get the full path for the old and new names
    old_file_path = os.path.join(folder2_path, filename)
    new_file_path = os.path.join(folder1_path, new_filename)

    # Rename and move the file to folder1
    shutil.move(old_file_path, new_file_path)

    print(f'Renamed and moved: {filename} to {new_filename} in {folder1_path}')