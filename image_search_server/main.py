from fastapi import FastAPI, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse
import os

app = FastAPI()

SCRAPED_IMAGES_DIR = Path(os.getenv("SCRAPED_IMAGES_DIR", "scraped_images"))
SCRAPED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000/scraper/images/")


@app.get("/search-images/")
async def search_images(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    image_files = [file.name for file in SCRAPED_IMAGES_DIR.glob(
        "*") if file.is_file()]
    matching_files = [
        file for file in image_files if query.lower() in file.lower()]

    if not matching_files:
        raise HTTPException(status_code=404, detail="No matching images found")

    matching_image_urls = [f"{BASE_URL}{file}" for file in matching_files]
    return {"matching_images": matching_image_urls}


@app.get("/scraper/images/{image_name}")
async def get_image(image_name: str):
    try:
        image_path = SCRAPED_IMAGES_DIR / image_name
        print(f"Image Path: {image_path}")  # Log the image path for debugging
        if image_path.exists() and image_path.is_file():
            return FileResponse(image_path)
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving the image: {str(e)}")


@app.get("/")
async def read_root():
    return {"status": "Server is running", "scraped_images_dir": str(SCRAPED_IMAGES_DIR), "base_url": BASE_URL}
