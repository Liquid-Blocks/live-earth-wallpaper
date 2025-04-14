import ctypes
import os
import requests
from datetime import datetime
from PIL import Image, ImageOps
import warnings

Image.MAX_IMAGE_PIXELS = None  # disables the warning
warnings.simplefilter('ignore', Image.DecompressionBombWarning)

path_to_images = "C:/Users/FredericCote/Desktop/projects/goes-east-wallpaper/"
target_resolution = (3840, 2160)
globe_resolution = (1080, 1080)

def download_goes_image(save_path):
    image_url = "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg"
    print(f"[INFO] Downloading image from: {image_url}")
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"[SUCCESS] Image saved to: {save_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to download image: {e}")
        return False

def resize_and_pad_image(image_path, final_path, target_res, globe_res):
    print(f"[INFO] Processing image to fit {target_res}")
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
            print(f"[SUCCESS] Image resized and saved to: {final_path}")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to resize/pad image: {e}")
        return False


def set_wallpaper(image_path):
    print(f"[INFO] Setting image as wallpaper: {image_path}")
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    if result:
        print("[SUCCESS] Wallpaper set successfully.")
    else:
        print("[ERROR] Failed to set wallpaper.")

if __name__ == "__main__":
    original_path = os.path.join(path_to_images, 'goes_original.jpg')
    final_path = os.path.join(path_to_images, 'goes_wallpaper.jpg')

    if download_goes_image(original_path):
        if resize_and_pad_image(original_path, final_path, target_resolution, globe_resolution):
            set_wallpaper(final_path)
