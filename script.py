import ctypes
import os
import requests
from datetime import datetime
from PIL import Image, ImageOps
import warnings
import logging

Image.MAX_IMAGE_PIXELS = None  # disables the warning
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

path_to_images = "C:/Users/FredericCote/Desktop/projects/goes-east-wallpaper/"
log_file_path = os.path.join(path_to_images, 'log.txt')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        # logging.StreamHandler() # Uncomment this line to also print logs to console
    ]
)

target_resolution = (3840, 2160)
globe_resolution = (1080, 1080)

def download_goes_image(save_path):
    image_url = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg"
    logging.info(f"Downloading image from: {image_url}")
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Image saved to: {save_path}")
        return True
    except Exception as e:
        logging.exception(f"Failed to download image: {e}")
        return False

def resize_and_pad_image(image_path, final_path, target_res, globe_res):
    logging.info(f"Processing image to fit {target_res}")
    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            img = img.resize(globe_res, Image.LANCZOS)

            # Create new black background
            new_img = Image.new("RGB", target_res, (1, 1, 1))

            # Calculate top offset to center the image vertically
            paste_y = (target_res[1] - globe_res[1]) // 2
            paste_x = (target_res[0] - globe_res[0]) // 2

            new_img.paste(img, (paste_x, paste_y))

            new_img.save(final_path)
            logging.info(f"Image resized and saved to: {final_path}")
            return True
    except Exception as e:
        logging.exception(f"Failed to resize/pad image: {e}")
        return False


def set_wallpaper(image_path):
    logging.info(f"Setting image as wallpaper: {image_path}")
    # Ensure the path is absolute for ctypes
    absolute_image_path = os.path.abspath(image_path)
    logging.info(f"Absolute path for wallpaper: {absolute_image_path}")
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_image_path, 3)
    if result:
        logging.info("Wallpaper set successfully.")
    else:
        # Get error details if available (Windows specific)
        error_code = ctypes.GetLastError()
        logging.error(f"Failed to set wallpaper. SystemParametersInfoW returned {result}. Error code: {error_code}")


if __name__ == "__main__":
    logging.info("Script execution started.")
    original_path = os.path.join(path_to_images, 'goes_original.jpg')
    final_path = os.path.join(path_to_images, 'goes_wallpaper.jpg')

    if download_goes_image(original_path):
        if resize_and_pad_image(original_path, final_path, target_resolution, globe_resolution):
            set_wallpaper(final_path)
        else:
            logging.error("Resize and pad failed, skipping wallpaper set.")
    else:
        logging.error("Download failed, skipping resize and wallpaper set.")
    logging.info("Script execution finished.")
