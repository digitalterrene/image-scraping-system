# 🌟 Comprehensive Multi-Service System

This project features a suite of interconnected services designed to simplify operations involving **database management**, **dynamic content handling**, and **third-party integrations** like **WordPress**. Powered by **FastAPI**, the system offers robust APIs for scalable and efficient performance.

---

## 📑 Table of Contents

- [🌟 Comprehensive Multi-Service System](#-comprehensive-multi-service-system)
  - [📑 Table of Contents](#-table-of-contents)
  - [1. 🚀 Servers Overview](#1--servers-overview)
    - [🔹 Dynamic Database Saver](#-dynamic-database-saver)
    - [🔹 Dynamic Image Saver](#-dynamic-image-saver)
    - [🔹 Additional Planned Services](#-additional-planned-services)
  - [2. ✨ Features](#2--features)
  - [3. ⚙️ Setup and Installation](#3-️-setup-and-installation)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [4. 🔗 API Endpoints](#4--api-endpoints)
    - [🔹 Dynamic Database Saver](#-dynamic-database-saver-1)
    - [🔹 Dynamic Image Saver](#-dynamic-image-saver-1)
  - [5. 🗄️ Database Configuration](#5-️-database-configuration)
  - [6. 🌐 WordPress Integration](#6--wordpress-integration)
    - [Configuration Steps:](#configuration-steps)
    - [Supported Formats:](#supported-formats)
  - [7. 📂 Folder Structure](#7--folder-structure)
  - [8. 🔮 Future Enhancements](#8--future-enhancements)
  - [9. 🙌 Credits](#9--credits)

---

## 1. 🚀 Servers Overview

### 🔹 Dynamic Database Saver

- Dynamically connects to any database using API-supplied credentials.
- Supports operations like **saving**, **querying**, and **updating data**.
- Handles background tasks for non-blocking performance.

### 🔹 Dynamic Image Saver

- Automates saving images from a local directory to a **MySQL database**.
- Optionally uploads images to **WordPress** via REST API and saves the WordPress URL in the database.

### 🔹 Additional Planned Services

The modular design enables adding new services, such as:

- **User Management**
- **File Processing**
- **Enhanced Third-Party Integrations**

---

## 2. ✨ Features

- **Dynamic Database Connections**  
  Flexibly connect to and operate on any database using runtime-provided credentials.

- **Image Handling**  
  Batch-process images, save metadata, and optionally upload to WordPress.

- **Background Tasks**  
  Use asynchronous operations for faster and non-blocking workflows.

- **Error Handling**  
  Robust mechanisms to handle invalid paths, database issues, and API errors.

- **Scalability**  
  Designed for extensibility, allowing seamless integration of new services and endpoints.

---

## 3. ⚙️ Setup and Installation

### Prerequisites

- **Python** 3.9+
- **MySQL** or **MariaDB** database
- **WordPress** (for image upload integration)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/multi-service-system.git
   cd multi-service-system
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Each Server**  
   Start servers using `uvicorn`. Example for Dynamic Image Saver:

   ```bash
   uvicorn dynamic_image_saver:app --reload
   ```

4. **Access API Documentation**  
   Navigate to `/docs` for interactive API documentation:  
   Example: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 4. 🔗 API Endpoints

### 🔹 Dynamic Database Saver

- **POST /save-to-database/**  
  Dynamically connect to a database and save incoming data.

  **Parameters**:

  - Database credentials (`db_host`, `db_port`, `db_user`, `db_password`, `db_name`)
  - Data to save (JSON)

  **Response**:

  - Success or failure message after saving data.

---

### 🔹 Dynamic Image Saver

- **GET /**  
  Health check endpoint to verify server status.

- **POST /save-images-to-database/**  
  Save images and metadata to a database and optionally upload to WordPress.

  **Parameters**:

  - Directory path containing images.
  - Optional WordPress credentials (`wp_api_url`, `wp_user`, `wp_password`).

  **Response**:

  - Success message with details of processed images.

---

## 5. 🗄️ Database Configuration

- Uses **SQLAlchemy** for ORM with **MySQL** database support.
- Dynamically connects to the database specified in the request.
- Automatically creates tables based on ORM models.

**Example Table (Dynamic Image Saver):**

```sql
CREATE TABLE images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255),
    description TEXT,
    wp_url VARCHAR(255)
);
```

---

## 6. 🌐 WordPress Integration

The **Dynamic Image Saver** supports uploading images to **WordPress** using its REST API.

### Configuration Steps:

1. Provide the WordPress API endpoint (e.g., `/wp-json/wp/v2/media`).
2. Use a valid WordPress username and password for authentication.

### Supported Formats:

- JPEG
- PNG
- GIF

---

## 7. 📂 Folder Structure

```plaintext
project-root/
│
├── dynamic_database_saver.py  # Server for saving data to any database.
├── dynamic_image_saver.py     # Server for image handling and saving.
├── requirements.txt           # Python dependencies.
├── README.md                  # Project documentation.
└── ...                        # Additional services and modules.
```

---

## 8. 🔮 Future Enhancements

- **Authentication and Authorization**  
  Add OAuth2 for secure access to APIs.

- **Cloud Storage Integration**  
  Support for AWS S3, Google Cloud Storage, and Azure Blob Storage.

- **User Management API**  
  Extend functionality to manage users and roles.

- **Custom Query Builder**  
  Provide a user-friendly frontend for building dynamic queries.

---

## 9. 🙌 Credits

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Third-Party Integration**: [WordPress REST API](https://developer.wordpress.org/rest-api/)

---

💡 _Feel free to contribute, suggest features, or report issues!_  
📧 Contact: [Your Email]
