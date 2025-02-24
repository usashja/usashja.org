import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# The URL of the website to copy
website_url = "https://usashja.org"

# Create a directory to save the website
output_dir = "usashja_website"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def save_file(url, file_path):
    """Save file from a URL to the specified file path."""
    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)

def download_website(url, output_dir):
    """Download the HTML content of the website and save it to the output directory."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Save the main HTML page
    main_html_path = os.path.join(output_dir, "index.html")
    with open(main_html_path, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    # Download and save all linked assets (e.g., images, CSS files)
    for tag in soup.find_all(["img", "link", "script"]):
        src = tag.get("src") or tag.get("href")
        if src:
            asset_url = urljoin(url, src)
            asset_path = os.path.join(output_dir, os.path.basename(asset_url))
            save_file(asset_url, asset_path)

# Start the download
download_website(website_url, output_dir)
print(f"Website {website_url} has been copied to {output_dir}")