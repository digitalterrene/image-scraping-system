from fastapi import FastAPI, HTTPException, Form, BackgroundTasks
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import shutil
import requests
from typing import Optional

# FastAPI app
app = FastAPI()

# SQLAlchemy ORM setup
Base = declarative_base()


class Image(Base):
    """
    ORM model for the images table.
    """
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    wp_url = Column(String(255), nullable=True)  # WordPress URL of the uploaded image


def get_session_maker(db_url: str):
    """
    Create and return a SQLAlchemy session maker for a given database URL.
    """
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal


def save_image_to_db(session_maker, file_name: str, title: str, description: str, wp_url: Optional[str]):
    """
    Save image metadata to the database.
    """
    session = session_maker()
    new_image = Image(file_name=file_name, title=title, description=description, wp_url=wp_url)
    session.add(new_image)
    session.commit()
    session.close()


def upload_to_wordpress(file_path: Path, wp_api_url: str, wp_user: str, wp_password: str):
    """
    Upload an image to WordPress and return the URL.
    """
    try:
        files = {"file": open(file_path, "rb")}
        response = requests.post(
            wp_api_url,
            files=files,
            auth=(wp_user, wp_password),
            timeout=15
        )
        if response.status_code == 201:
            return response.json()["source_url"]
        else:
            raise Exception(f"Failed to upload to WordPress: {response.text}")
    except Exception as e:
        raise Exception(f"Error uploading image to WordPress: {e}")


@app.post("/save-images-to-database/")
async def save_images_to_db(
    background_tasks: BackgroundTasks,
    db_host: str = Form(...),
    db_port: int = Form(...),
    db_user: str = Form(...),
    db_password: str = Form(...),
    db_name: str = Form(...),
    image_dir: str = Form(...),
    wp_api_url: Optional[str] = Form(None),
    wp_user: Optional[str] = Form(None),
    wp_password: Optional[str] = Form(None),
):
    """
    Save all images in the specified directory to the database and optionally upload to WordPress.
    """
    try:
        # Build the database URL
        db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        session_maker = get_session_maker(db_url)

        # Process all images in the specified directory
        image_directory = Path(image_dir)
        if not image_directory.exists() or not image_directory.is_dir():
            raise HTTPException(status_code=400, detail="Invalid image directory")

        for image_file in image_directory.iterdir():
            if image_file.is_file() and image_file.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif"]:
                file_name = image_file.name

                # Upload to WordPress if credentials are provided
                wp_url = None
                if wp_api_url and wp_user and wp_password:
                    wp_url = upload_to_wordpress(image_file, wp_api_url, wp_user, wp_password)

                # Save to database
                background_tasks.add_task(save_image_to_db, session_maker, file_name, file_name, "Image description", wp_url)

        return {"message": "All images saved to the database and WordPress (if provided)."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    """
    Basic health check endpoint.
    """
    return {"status": "Server is running"}
