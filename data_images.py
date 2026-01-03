import os
import time
import requests
import pandas as pd
from tqdm import tqdm

MAPBOX_TOKEN = "pk.eyJ1IjoiYWtoaWwxMjEyIiwiYSI6ImNtanZlY3g4cjFwa3IzZnFzbGU2eHFjd3AifQ.FeYlqYtomlM7fSYz7rWkjQ"

OUTPUT_DIR = "data/images/train"

ZOOM_LEVEL = 18
IMAGE_SIZE = 256   
os.makedirs(OUTPUT_DIR, exist_ok=True)
print("Loading dataset...")

data = pd.read_excel("train(1).xlsx")[["id", "lat", "long"]]
print(f"Records found: {len(data)}")

def download_satellite_tile(lat, lon, file_name):
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
        f"{lon},{lat},{ZOOM_LEVEL},0/{IMAGE_SIZE}x{IMAGE_SIZE}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(file_name, "wb") as img:
                img.write(response.content)
            return True

        return False

    except requests.exceptions.RequestException:
        return False
print("\nStarting image download...\n")

failed_downloads = []

for _, row in tqdm(data.iterrows(), total=len(data)):

    image_path = os.path.join(OUTPUT_DIR, f"{row['id']}.png")

    if os.path.exists(image_path):
        continue

    success = download_satellite_tile(
        lat=row["lat"],
        lon=row["long"],
        file_name=image_path
    )

    if not success:
        failed_downloads.append(row["id"])

    time.sleep(0.2)      
print("\nDownload complete!")

print(f"Images saved: {len(data) - len(failed_downloads)}")
print(f"Failed downloads: {len(failed_downloads)}")
