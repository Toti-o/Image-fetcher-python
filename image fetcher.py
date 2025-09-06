import requests
import os
from urllib.parse import urlparse
from hashlib import md5

# Directory to save images
SAVE_DIR = "Fetched_Images"

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "downloaded_image.jpg"
    return filename

def download_image(url, downloaded_hashes):
    try:
        # Fetch the image with headers to mimic a browser
        headers = {"User-Agent": "UbuntuImageFetcher/1.0 (+https://example.com)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Check content type
        if 'image' not in response.headers.get('Content-Type', ''):
            print(f"✗ Skipped: URL does not point to an image -> {url}")
            return

        # Calculate hash to prevent duplicates
        file_hash = md5(response.content).hexdigest()
        if file_hash in downloaded_hashes:
            print(f"✗ Duplicate image detected, skipping -> {url}")
            return
        downloaded_hashes.add(file_hash)

        # Create directory if not exists
        os.makedirs(SAVE_DIR, exist_ok=True)

        # Save image
        filename = get_filename_from_url(url)
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls = input("Please enter image URLs separated by commas: ").split(',')
    urls = [url.strip() for url in urls if url.strip()]

    downloaded_hashes = set()
    for url in urls:
        download_image(url, downloaded_hashes)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
