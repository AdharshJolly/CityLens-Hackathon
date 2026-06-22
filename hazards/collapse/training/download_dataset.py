import ssl
import urllib.request
import zipfile
import os

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://app.roboflow.com/ds/hkaHzPdAlx?key=B1wtYENVmW"

print("Downloading dataset...")
urllib.request.urlretrieve(url, "collapse_dataset.zip")
print("Download complete! Extracting...")

with zipfile.ZipFile("collapse_dataset.zip", "r") as z:
    z.extractall("data/collapse")

print("Extraction complete!")

# Check how many images we got
train_count = len(os.listdir("data/collapse/train/images"))
print(f"Train images: {train_count}")