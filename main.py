# main.py (Root folder)

from fastapi import FastAPI, APIRouter
from scraper_server.main import app as scraper_app
from image_search_server.main import app as image_search_app

# Create the main FastAPI app
main_app = FastAPI()

# Create routers for sub-apps
scraper_router = APIRouter()
image_search_router = APIRouter()
converter_router = APIRouter()
dynamic_image_router = APIRouter()

# Include all routes from the scraper server under /scraper
scraper_router.include_router(scraper_app.router, prefix="/scraper")
image_search_router.include_router(
    image_search_app.router, prefix="/image-search")

# Add the routers to the main app
main_app.include_router(scraper_router)
main_app.include_router(image_search_router)


@main_app.get("/")
async def root():
    """
    Root route for the main server.
    """
    return {
        "status": "Main server is running",
        "routes": [
            "/scraper",
            "/image-search",
        ],
    }
