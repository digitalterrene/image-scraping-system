````markdown
# 🌐 Image Scraper Service - `scraper_server`

The `scraper_server` is a Python-based **FastAPI** service designed to download images from a list of provided URLs. This service accepts a list of image URLs via a **POST** request, fetches the images, and saves them to a local `downloads/` directory.

---

## 📑 Features

- **Scrape Images**: Accepts a list of URLs and downloads the corresponding images.
- **Health Check**: Verifies that the server is running and operational.
- **Directory Management**: Automatically creates a `downloads/` directory if it doesn't exist to store the images.

---

## 🔗 API Endpoints

### 1. **GET /**

**Description**:  
Health check endpoint to verify that the server is running.

**Response**:

- `status`: Message indicating the server's status.
- `downloads_dir`: Path to the directory where images are saved.

**Example Response**:

```json
{
  "status": "Server is running",
  "downloads_dir": "downloads"
}
```
````

---

### 2. **POST /download-images/**

**Description**:  
Downloads images from the provided URLs and saves them to the `downloads/` directory.

**Request Body**:

- `urls` (list of `HttpUrl`, required): A list of valid HTTP/HTTPS image URLs.

**Example Request**:

```json
{
  "urls": ["https://example.com/image1.jpg", "https://example.com/image2.png"]
}
```

**Response**:

- `message`: Confirmation message indicating that all images were downloaded successfully.
- `saved_to`: The directory where images were saved.

**Example Response**:

```json
{
  "message": "All images downloaded successfully",
  "saved_to": "downloads"
}
```

**Error Handling**:

- **`500 Internal Server Error`**: Returned if a URL cannot be downloaded. The error message provides details about the failed URL.

**Example Error Response**:

```json
{
  "detail": "Failed to download https://example.com/image.jpg: [Error details]"
}
```

---

## 📁 Directory Structure

### 1. **`downloads/`**

The directory where downloaded images are saved. This directory is automatically created if it doesn't exist.

---

## 🚀 Running the Server

### 1. **Install Dependencies**

To install the required dependencies, run:

```bash
pip install fastapi pydantic requests uvicorn
```

### 2. **Start the Server**

To run the server, use the following command:

```bash
uvicorn scraper_server:app --reload
```

### 3. **Access the Server**

- **Health Check**: Open a browser or API testing tool and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
- **API Documentation**: Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📝 Notes

- Ensure the URLs provided are publicly accessible and point directly to image files (e.g., `https://example.com/image.jpg`).
- For large-scale use, consider implementing **rate-limiting** to avoid overwhelming the server and optimizing error handling for robustness.
- Customize the `downloads/` directory path in the code if a different directory is desired for saving images.

---
