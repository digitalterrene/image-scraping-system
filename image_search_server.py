from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import List
from fastapi.responses import FileResponse
import os

# Create the FastAPI app
app = FastAPI()

# Define the path to the converted images folder
CONVERTED_IMAGES_DIR = Path("converted")
CONVERTED_IMAGES_DIR.mkdir(exist_ok=True)  # Ensure the folder exists

# Define the base URL for accessing the images
# Update this to your actual server URL when deploying (e.g., "http://localhost:8000/images/")
BASE_URL = "http://localhost:8000/images/"

@app.get("/search-images/")
async def search_images(query: str):
    """
    Search for images in the converted folder that contain the query string in their name.
    """
    try:
        # Get all image files in the folder
        image_files = [file.name for file in CONVERTED_IMAGES_DIR.glob("*") if file.is_file()]

        # Filter files by query (case-insensitive)
        matching_files = [file for file in image_files if query.lower() in file.lower()]

        if not matching_files:
            raise HTTPException(status_code=404, detail="No matching images found")

        # Create URLs for the matching files
        matching_image_urls = [BASE_URL + file for file in matching_files]

        return {"matching_images": matching_image_urls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching images: {str(e)}")

@app.get("/images/{image_name}")
async def get_image(image_name: str):
    """
    Serve the image from the converted folder when requested.
    """
    image_path = CONVERTED_IMAGES_DIR / image_name
    if image_path.exists() and image_path.is_file():
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Image not found")

@app.get("/")
async def read_root():
    """
    Basic health check.
    """
    return {"status": "Server is running", "converted_images_dir": str(CONVERTED_IMAGES_DIR)}
