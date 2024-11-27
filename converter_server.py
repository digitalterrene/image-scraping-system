from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import Literal
from PIL import Image  # Pillow library for image conversion

# Create the FastAPI app
app = FastAPI()

# Directory where images are saved
DOWNLOAD_DIR = Path("downloads")
CONVERTED_DIR = Path("converted")
CONVERTED_DIR.mkdir(exist_ok=True)  # Create a directory for converted images if not exists


# Pydantic model to validate input
class ConversionRequest(BaseModel):
    format: Literal["png", "jpg", "jpeg", "webp", "bmp", "gif"]  # Supported formats


@app.post("/convert-images/")
async def convert_images(request: ConversionRequest):
    """
    Converts all images in the downloads directory to the specified format.
    """
    if not DOWNLOAD_DIR.exists():
        raise HTTPException(status_code=404, detail="Downloads directory does not exist")

    converted_files = []

    for image_file in DOWNLOAD_DIR.iterdir():
        if image_file.is_file() and image_file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"]:
            new_file_name = image_file.stem + f".{request.format}"
            new_file_path = CONVERTED_DIR / new_file_name

            try:
                with Image.open(image_file) as img:
                    img = img.convert("RGB")  # Convert to RGB format (ignoring alpha channel)
                    img.save(new_file_path, format=request.format.upper())
                    converted_files.append(str(new_file_path))

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to convert {image_file.name}: {str(e)}")

    return {
        "message": "All images converted successfully",
        "converted_files": converted_files,
        "output_dir": str(CONVERTED_DIR)
    }


@app.get("/")
async def read_root():
    """
    Basic health check.
    """
    return {"status": "Image Converter is running", "converted_dir": str(CONVERTED_DIR)}
