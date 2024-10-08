import re
import constants
import os
import requests
import pandas as pd
import multiprocessing
import time
from time import time as timer
from tqdm import tqdm
import numpy as np
from pathlib import Path
from functools import partial
import urllib
from PIL import Image

# Enhanced unit normalization to handle common mistakes
def common_mistake(unit):
    unit_mapping = {
        'lbs': 'pound',  # Handle 'lbs' to 'pound'
        'feet': 'foot',  # Handle 'feet' to 'foot'
        'ter': 'tre',    # Handle 'ter' to 'tre'
        # Add more mappings as needed
    }
    normalized_unit = unit_mapping.get(unit, unit)
    if normalized_unit in constants.allowed_units:
        return normalized_unit
    return unit  # Default, if no match is found

# Enhanced error message for parse_string
def parse_string(s):
    s_stripped = "" if s == None or str(s) == 'nan' else s.strip()
    if s_stripped == "":
        return None, None
    pattern = re.compile(r'^-?\d+(\.\d+)?\s+[a-zA-Z\s]+$')
    if not pattern.match(s_stripped):
        raise ValueError(f"Invalid format in {s}")
    
    parts = s_stripped.split(maxsplit=1)
    number = float(parts[0])
    unit = common_mistake(parts[1])
    
    if unit not in constants.allowed_units:
        raise ValueError(f"Invalid unit [{unit}] found in string '{s}'. Allowed units: {constants.allowed_units}")
    
    return number, unit

# Placeholder image creation
def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
    except Exception as e:
        return

# Image downloading with retries and enhanced error handling
def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    if os.path.exists(image_save_path):
        return

    for attempt in range(retries):
        try:
            urllib.request.urlretrieve(image_link, image_save_path)
            return
        except Exception as e:
            print(f"Failed to download {image_link} on attempt {attempt+1}. Retrying...")
            time.sleep(delay)

    print(f"Failed to download {image_link}. Creating placeholder.")
    create_placeholder_image(image_save_path)  # Create a placeholder if the download fails

# Image downloading in parallel with multiprocessing support
def download_images(image_links, download_folder, allow_multiprocessing=True):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if allow_multiprocessing:
        download_image_partial = partial(download_image, save_folder=download_folder, retries=3, delay=3)

        with multiprocessing.Pool(64) as pool:
            list(tqdm(pool.imap(download_image_partial, image_links), total=len(image_links)))
            pool.close()
            pool.join()
    else:
        for image_link in tqdm(image_links, total=len(image_links)):
            download_image(image_link, save_folder=download_folder, retries=3, delay=3)
