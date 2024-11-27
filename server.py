from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from pathlib import Path

# Create the FastAPI app
app = FastAPI()

# Define a directory for image downloads
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)  # Create the downloads directory if it doesn't exist


# Pydantic model to validate input
class ImageLinks(BaseModel):
    urls: list[HttpUrl]  # Ensure all URLs are valid HTTP/HTTPS links


@app.post("/download-images/")
async def download_images(links: ImageLinks):
    """
    Downloads images from the provided URLs and saves them to the downloads directory.
    """
    for url in links.urls:
        # Convert HttpUrl to string before using string methods
        url_str = str(url)
        file_name = url_str.split("/")[-1].split("?")[0]
        file_path = DOWNLOAD_DIR / file_name  # Save file in the downloads directory

        try:
            response = requests.get(url_str, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors

            with open(file_path, "wb") as f:
                f.write(response.content)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to download {url_str}: {str(e)}")

    return {"message": "All images downloaded successfully", "saved_to": str(DOWNLOAD_DIR)}


@app.get("/")
async def read_root():
    """
    Basic health check.
    """
    return {"status": "Server is running", "downloads_dir": str(DOWNLOAD_DIR)}
