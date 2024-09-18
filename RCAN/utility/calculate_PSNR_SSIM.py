import os
import numpy as np
from skimage.metrics import structural_similarity
from skimage.color import rgb2ycbcr
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.signal import gaussian

def load_images_from_folder(folder):
    images = {}
    for filename in os.listdir(folder):
        img = Image.open(os.path.join(folder, filename))
        if img is not None:
            img_arr = np.array(img)
            common_name = filename.split('_')[0].split('.')[0]
            images[common_name] = img_arr
    return images

def ssim_index(img1, img2):
    # Ensure the images are floating-point and within [0, 255]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)

    # Default constants
    K = [0.01, 0.03]
    L = 255  # Dynamic range of the pixel values

    # Calculate constants C1 and C2
    C1 = (K[0] * L) ** 2
    C2 = (K[1] * L) ** 2

    # Define a Gaussian window
    window_size = 11
    window_sigma = 1.5
    gaussian_1d = gaussian(window_size, std=window_sigma)
    window = np.outer(gaussian_1d, gaussian_1d)
    window /= np.sum(window)

    # Calculate means (mu1, mu2)
    mu1 = gaussian_filter(img1, window_sigma)
    mu2 = gaussian_filter(img2, window_sigma)

    # Calculate squares of means
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    # Calculate variances and covariances
    sigma1_sq = gaussian_filter(img1 ** 2, window_sigma) - mu1_sq
    sigma2_sq = gaussian_filter(img2 ** 2, window_sigma) - mu2_sq
    sigma12 = gaussian_filter(img1 * img2, window_sigma) - mu1_mu2

    # Calculate SSIM map
    if C1 > 0 and C2 > 0:
        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / \
                   ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    else:
        numerator1 = 2 * mu1_mu2 + C1
        numerator2 = 2 * sigma12 + C2
        denominator1 = mu1_sq + mu2_sq + C1
        denominator2 = sigma1_sq + sigma2_sq + C2

        ssim_map = np.ones(mu1.shape)
        valid = (denominator1 * denominator2) > 0
        ssim_map[valid] = (numerator1[valid] * numerator2[valid]) / \
                          (denominator1[valid] * denominator2[valid])

        valid = denominator1 != 0
        ssim_map[valid & ~denominator2] = numerator1[valid & ~denominator2] / denominator1[valid & ~denominator2]

    # Mean SSIM computation
    mssim = ssim_map.mean()

    return mssim

def crop_border(image, scale_factor, border_height, border_weight):
    """Crop the image by removing a border of border_size from each side."""
    return image[scale_factor:-border_height, scale_factor:-border_weight]

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    psnr_value = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr_value

def calculate_average_psnr_ssim(hr_folder, sr_folder, scale_factor):
    hr_images = load_images_from_folder(hr_folder)
    sr_images = load_images_from_folder(sr_folder)

    psnr_values = []
    ssim_values = []

    for common_name in hr_images:
        if common_name in sr_images:
            hr_image = hr_images[common_name].astype(np.float32)
            sr_image = sr_images[common_name].astype(np.float32)

            if hr_image.shape[2] == 3:
                hr_y = rgb2ycbcr(hr_image)[:, :, 0] / 255.0
                sr_y = rgb2ycbcr(sr_image)[:, :, 0] / 255.0
            else:
                hr_y = hr_image
                sr_y = sr_image

            # Crop the border area

            height_hr, width_hr = hr_y.shape
            print(f"HR Before  Width: {width_hr}, Height: {height_hr}")
            height_sr, width_sr = sr_y.shape
            print(f"SR Before  Width: {width_sr}, Height: {height_sr}")
            if height_hr == height_sr and width_hr == width_sr:
                hr_y = crop_border(hr_y, scale_factor, scale_factor, scale_factor)
                sr_y = crop_border(sr_y, scale_factor, scale_factor, scale_factor)
            if height_hr > height_sr and width_hr == width_sr:
                border_height = (int)(scale_factor - ((height_hr - height_sr)))
                hr_y = crop_border(hr_y, scale_factor, scale_factor, scale_factor)
                sr_y = crop_border(sr_y, scale_factor, border_height, scale_factor)
                height_sr, width_sr = sr_y.shape
                print(f"SR After height_hr >> height_sr   Width: {width_sr}, Height: {height_sr}")
            if height_hr == height_sr and width_hr > width_sr:
                border_width = (int)(scale_factor- ((width_hr - width_sr)))
                hr_y = crop_border(hr_y, scale_factor, scale_factor, scale_factor)
                sr_y = crop_border(sr_y, scale_factor, scale_factor , border_width)
                height_sr, width_sr = sr_y.shape
                print(f"SR After width_hr >> width_sr After  Width: {width_sr}, Height: {height_sr}")
            height_hr, width_hr = hr_y.shape
            print(f"HR After  Width: {width_hr}, Height: {height_hr}")
            height_sr, width_sr = sr_y.shape
            print(f"SR After  Width: {width_sr}, Height: {height_sr}")
            # Calculate PSNR
            current_psnr = calculate_psnr(hr_y, sr_y)
            psnr_values.append(current_psnr)

            # Calculate SSIM
            ssim_value = ssim_index(hr_y, sr_y)
            ssim_values.append(ssim_value)
        else:
            print(f"Super-resolved image for {common_name} not found in SR folder.")

    average_psnr = np.mean(psnr_values)
    average_ssim = np.mean(ssim_values)

    return average_psnr, average_ssim

def save_results_to_file(sr_folder, average_psnr, average_ssim, exp_name):
    sr_folder_name = os.path.basename(os.path.normpath(sr_folder))

    results = (
        f"Results for {sr_folder_name}:\n"
        f"Average PSNR: {average_psnr}\n"
        f"Average SSIM: {average_ssim}\n"
    )

    output_file = f"{sr_folder_name}_{exp_name}_results.txt"

    with open(output_file, 'w') as file:
        file.write(results)

# Usage
scale_factor = 4  # Update this to your correct scale factor
hr_folder = f'/home/linuxu/Projects/RCAN/RCAN_TestCode/HR/Set5/x{scale_factor}'
exp_name = 'Exp26'

sr_folder = f'/home/linuxu/Projects/RCAN/RCAN_TestCode/SR/BI/{exp_name}/Set5/x{scale_factor}'

average_psnr, average_ssim = calculate_average_psnr_ssim(hr_folder, sr_folder, scale_factor)
save_results_to_file(sr_folder, average_psnr, average_ssim, exp_name)
