### Documentation for `dynamic_image_saver.py`

The `dynamic_image_saver.py` script is a FastAPI-based service designed to save image metadata to a database, with an optional feature to upload images to a WordPress site.

---

### Features

1. Save image metadata from a specified directory to a MySQL database.
2. Optionally upload images to a WordPress site using provided credentials.
3. Background tasks for asynchronous database operations.

---

### Endpoints

#### 1. `GET /`

**Description:**  
A basic health check endpoint to verify that the server is operational.

**Response:**

- `status`: Indicates whether the server is running.

**Example Response:**

```json
{
  "status": "Server is running"
}
```

---

#### 2. `POST /save-images-to-database/`

**Description:**  
Saves all images in the specified directory to a MySQL database. If WordPress credentials are provided, images are also uploaded to a WordPress site, and the resulting URL is stored in the database.

**Request Parameters (Form):**

- `db_host` (string, required): The database host address.
- `db_port` (integer, required): The database port (e.g., 3306).
- `db_user` (string, required): The database username.
- `db_password` (string, required): The database password.
- `db_name` (string, required): The name of the database.
- `image_dir` (string, required): The directory containing the images to process.
- `wp_api_url` (string, optional): The WordPress REST API URL for media upload.
- `wp_user` (string, optional): The WordPress username for authentication.
- `wp_password` (string, optional): The WordPress password for authentication.

**Response:**

- `message`: Indicates whether the operation was successful.

**Example Request:**

```bash
curl -X POST "http://127.0.0.1:8000/save-images-to-database/" \
-F "db_host=localhost" \
-F "db_port=3306" \
-F "db_user=root" \
-F "db_password=yourpassword" \
-F "db_name=image_database" \
-F "image_dir=/path/to/images" \
-F "wp_api_url=https://example.com/wp-json/wp/v2/media" \
-F "wp_user=admin" \
-F "wp_password=adminpassword"
```

**Example Response:**

```json
{
  "message": "All images saved to the database and WordPress (if provided)."
}
```

**Error Handling:**

- **400 Bad Request**: Returned if the `image_dir` does not exist or is invalid.
- **500 Internal Server Error**: Returned for database connection errors, WordPress upload failures, or other unexpected issues.

---

### Database Setup

- **Database URL:**  
  The database URL is dynamically generated based on the provided credentials.  
  Example:  
  `mysql+pymysql://db_user:db_password@db_host:db_port/db_name`

- **ORM Model:**  
  The service uses SQLAlchemy ORM for database interaction. The `images` table schema:

  ```sql
  CREATE TABLE images (
      id INT AUTO_INCREMENT PRIMARY KEY,
      file_name VARCHAR(255) NOT NULL UNIQUE,
      title VARCHAR(255),
      description TEXT,
      wp_url VARCHAR(255)
  );
  ```

- **Image Metadata Fields:**
  - `file_name`: The name of the image file.
  - `title`: The title of the image (defaults to the file name).
  - `description`: A description of the image (defaults to "Image description").
  - `wp_url`: The WordPress URL of the uploaded image (if applicable).

---

### WordPress Integration

- **Upload Functionality:**  
  If `wp_api_url`, `wp_user`, and `wp_password` are provided, images are uploaded to WordPress using the REST API. The returned `source_url` is stored in the database.

- **Authentication:**  
  The service uses Basic Authentication for WordPress API.

- **Supported Formats:**  
  The service supports common image formats: `.jpg`, `.jpeg`, `.png`, and `.gif`.

---

### Directory Requirements

- **Image Directory (`image_dir`):**  
  The directory must exist and contain valid image files for processing.

---

### How to Run the Server

1. **Install dependencies:**  
   Ensure you have the required libraries installed:

   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql requests
   ```

2. **Start the server:**  
   Run the following command:

   ```bash
   uvicorn dynamic_image_saver:app --reload
   ```

3. **Access the API:**  
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

---

### Notes

- **Background Tasks:**  
  The `BackgroundTasks` feature ensures that database operations do not block the main request cycle.

- **Error Handling:**  
  The service handles common errors, such as invalid directories, database connection issues, and WordPress upload failures.

- **Extensibility:**  
  The code can be extended to support additional image formats, metadata fields, or storage mechanisms (e.g., cloud storage).

---
