# GOES East Wallpaper Script

![GOES East Image](https://cdn.star.nesdis.noaa.gov/GOES19/ABI/FD/GEOCOLOR/latest.jpg)

This script downloads the latest GOES East image, resizes it, and sets it as the desktop wallpaper.

## Requirements

- Python 3.x
- `requests`
- `Pillow`

## Installation

To install the required packages, run:

```bash
pip install requests Pillow
```

## Usage

1. Clone the repository or download the script.
2. Ensure the path to images is correctly set in the script.
3. To change the resolution of the final wallpaper, modify the `target_resolution` variable in the script. For example, to set it to 1920x1080, change the line to:

   ```python
   target_resolution = (1920, 1080)
   ```

4. Run the script:

```bash
python script.py
```

## Logging

The script logs its activities to a file named `log.txt` in the specified image path.