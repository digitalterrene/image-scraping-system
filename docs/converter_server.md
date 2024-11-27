````markdown
# 🖼️ Image Converter Service - `converter_server.py`

The `converter_server.py` is a **FastAPI**-based service that streamlines image conversion tasks. It processes images from a `downloads/` directory, converts them to a specified format, and saves them in the `converted/` directory.

---

## 📑 Features

- Convert images in the `downloads/` directory to a target format.
- Save the converted images in the `converted/` directory.
- Includes a health check endpoint to verify server operation.

---

## 🔗 API Endpoints

### 1. **GET /**

**Description**:  
Health check endpoint to confirm that the server is operational.

**Response**:

- `status`: Indicates whether the server is running.
- `converted_dir`: Directory where converted images are saved.

**Example Response**:

```json
{
  "status": "Image Converter is running",
  "converted_dir": "converted"
}
```
````

---

### 2. **POST /convert-images/**

**Description**:  
Converts all images in the `downloads/` directory to the specified format.

**Request Body**:

- `format` (string, required): Target format for conversion.  
  Supported formats: `png`, `jpg`, `jpeg`, `webp`, `bmp`, `gif`.

**Response**:

- `message`: Success message after conversion.
- `converted_files`: List of paths for the converted images.
- `output_dir`: Directory path where converted images are saved.

**Example Request**:

```bash
curl -X POST "http://127.0.0.1:8000/convert-images/" \
-H "Content-Type: application/json" \
-d '{"format": "png"}'
```

**Example Response**:

```json
{
  "message": "All images converted successfully",
  "converted_files": ["converted/example1.png", "converted/example2.png"],
  "output_dir": "converted"
}
```

**Error Handling**:

- **`404 Not Found`**: Returned if the `downloads/` directory does not exist.
- **`500 Internal Server Error`**: Returned if an error occurs during image conversion.

---

## 📁 Directory Structure

### 1. **`downloads/`**

Source directory where images to be converted are stored.

> **Note**: This directory must exist and contain valid image files.

### 2. **`converted/`**

Target directory where converted images are saved.

> **Note**: This directory is created automatically if it does not exist.

---

## 🎨 Supported Formats

The service supports converting images to the following formats:

- **PNG**
- **JPG**
- **JPEG**
- **WEBP**
- **BMP**
- **GIF**

---

## 🚀 How to Run the Server

### 1. **Install Dependencies**

Ensure the required packages are installed:

```bash
pip install fastapi uvicorn pillow
```

### 2. **Start the Server**

Run the server using Uvicorn:

```bash
uvicorn converter_server:app --reload
```

### 3. **Access the API**

Open a browser or API testing tool and navigate to:

```
http://127.0.0.1:8000/docs
```

This URL provides an interactive API documentation interface.

---

## 📝 Notes

- **Input Directory**: Ensure the `downloads/` directory exists and contains images to convert before using the service.
- **Error Handling**: Unsupported file types or corrupt images will not be processed and may raise an exception.
- **Image Quality**: The service defaults to **RGB conversion**, which may not preserve alpha transparency for formats like PNG.

---

💡 _Contributions, bug reports, and suggestions are welcome!_

```

```
