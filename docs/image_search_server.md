Here’s the specific **README-style documentation** for `image_search_server.py`:

---

### Documentation for `image_search_server.py`

The `image_search_server.py` is a FastAPI-based service that enables users to search for and retrieve images stored in a local directory.

---

### Features

- Search for images in a local directory (`converted/`) based on a query string.
- Retrieve and serve images from the `converted/` directory.
- Perform a basic health check to verify server status.

---

### Endpoints

#### 1. `GET /`

**Description:**  
A health check endpoint to confirm the server is operational.

**Response:**

- `status`: Indicates if the server is running.
- `converted_images_dir`: The directory path where images are stored.

**Example Response:**

```json
{
  "status": "Server is running",
  "converted_images_dir": "converted"
}
```

---

#### 2. `GET /search-images/`

**Description:**  
Searches for images in the `converted/` directory containing the provided query string in their filenames.

**Query Parameter:**

- `query` (string, required): Case-insensitive substring to match against filenames.

**Response:**

- `matching_images`: A list of URLs for the images that match the query.

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/search-images/?query=example"
```

**Example Response:**

```json
{
  "matching_images": [
    "http://localhost:8000/images/example1.jpg",
    "http://localhost:8000/images/example2.png"
  ]
}
```

**Error Handling:**

- **404 Not Found**: Returned when no images match the query.
- **500 Internal Server Error**: Returned if an error occurs during the search.

---

#### 3. `GET /images/{image_name}`

**Description:**  
Retrieves a specific image from the `converted/` directory.

**Path Parameter:**

- `image_name` (string, required): The exact filename of the image.

**Response:**

- Returns the requested image file.

**Example Request:**

```bash
curl -X GET "http://127.0.0.1:8000/images/example1.jpg"
```

**Error Handling:**

- **404 Not Found**: Returned if the specified image does not exist in the directory.

---

### Directory Structure

- **`converted/`**:  
  Stores the images that can be searched or retrieved.  
  This folder is created automatically if it does not exist.

---

### How to Run the Server

1. **Install dependencies**:  
   Ensure you have FastAPI and Uvicorn installed. Run:

   ```bash
   pip install fastapi uvicorn
   ```

2. **Start the server**:  
   Use the following command to start the server:

   ```bash
   uvicorn image_search_server:app --reload
   ```

3. **Access the API**:  
   Open your browser or API testing tool and navigate to:  
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   This provides an interactive API documentation interface.

---

### Notes

- **Customization**: Update the `BASE_URL` variable in the code to reflect your server's URL when deploying.
- **Directory Management**: Ensure the `converted/` directory contains the images to be searched or retrieved.

---
