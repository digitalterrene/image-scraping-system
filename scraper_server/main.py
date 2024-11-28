import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib.parse import urljoin, urlparse
from typing import List
from pathlib import Path
import aiofiles
import httpx
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Create the FastAPI app
app = FastAPI()

# Define the base directory for the app
BASE_DIR = Path(__file__).resolve().parent.parent
SCRAPED_IMAGES_DIR = BASE_DIR / "scraped_images"
SCRAPED_IMAGES_DIR.mkdir(exist_ok=True)

# Mount static folder to serve images
app.mount("/scraper/images",
          StaticFiles(directory=SCRAPED_IMAGES_DIR), name="images")

# Model to validate input


class ScrapeRequest(BaseModel):
    url: str


async def download_image(url: str, file_path: Path):
    """
    Downloads an image from a URL and saves it to the specified file path.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200 and response.headers["content-type"].startswith("image/"):
            async with aiofiles.open(file_path, 'wb') as file:
                await file.write(response.content)
        else:
            raise ValueError(
                f"Invalid image or non-200 status code from {url}")


@app.post("/scrape-images/")
async def scrape_images(request: ScrapeRequest):
    """
    Scrapes the images from the provided URL, downloads them,
    and returns a list of saved image URLs.
    """
    url = request.url

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <img> tags on the page
        img_tags = soup.find_all('img')

        # Extract image URLs
        img_urls = [urljoin(url, img['src'])
                    for img in img_tags if 'src' in img.attrs]

        if not img_urls:
            raise HTTPException(
                status_code=404, detail="No images found on the webpage.")

        saved_image_paths = []

        # Download and save each image to the scraped_images folder
        for img_url in img_urls:
            # Extract the image file name from the URL
            img_name = Path(urlparse(img_url).path).name
            if not img_name:  # If name extraction fails, skip
                continue

            file_path = SCRAPED_IMAGES_DIR / img_name

            try:
                # Download and save the image asynchronously
                await download_image(img_url, file_path)
                saved_image_paths.append(str(file_path))
            except Exception as e:
                print(f"Failed to download image from {img_url}: {str(e)}")

        if not saved_image_paths:
            raise HTTPException(
                status_code=500, detail="Failed to download any images.")

        # Return the file paths as URLs with prefix
        return {
            "message": "Images scraped and saved successfully.",
            "saved_images": [
                f"http://localhost:8000/scraper/images/{Path(path).name}" for path in saved_image_paths
            ]
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=400, detail=f"Error fetching the webpage: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/images/")  # To list all images
async def get_all_images():
    """
    Returns a list of URLs of all images in the scraped_images directory.
    """
    image_urls = []

    for image_file in SCRAPED_IMAGES_DIR.iterdir():
        if image_file.is_file():
            image_urls.append(
                f"http://localhost:8000/scraper/images/{image_file.name}")

    if image_urls:
        return {"images": image_urls}
    else:
        raise HTTPException(status_code=404, detail="No images found.")


@app.get("/images/{filename}")  # To serve a specific image
async def get_image(filename: str):
    """
    Serves an image file from the scraped_images directory.
    """
    file_path = SCRAPED_IMAGES_DIR / filename

    if file_path.exists():
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")


@app.get("/")
async def read_root():
    """
    Basic health check route
    """
    return {"status": "Scraper server is running"}
