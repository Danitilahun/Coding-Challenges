# URL Shortener API Documentation

This documentation provides a comprehensive guide to the URL Shortener API. It explains all available endpoints, expected input/output, and testing steps. Designed for readability, it also includes testing instructions and interactive documentation access.

---

## **Getting Started**

### **Base URL**
The base URL for the API is:
```
http://127.0.0.1:8000
```

### **Interactive Documentation**
FastAPI provides interactive Swagger documentation and ReDoc documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These allow you to test the API endpoints interactively.

---

## **Technology Stack**

### **1. Shortening Algorithm**
- **Algorithm**: The URL shortener uses a hashing-based algorithm.
  - It hashes the input URL using **SHA-256**.
  - The hash is encoded in **Base64** for compactness.
  - A random shuffle is applied to introduce additional entropy.
  - Finally, the resulting string is truncated to **7 characters** for the short key.
  
### **2. Database**
- **Type**: SQLite (Lightweight, file-based database).
- **ORM**: SQLAlchemy is used for defining models and querying the database.
- **Schema**:
  - `id` (Integer, Primary Key): Unique identifier for each URL.
  - `key` (String, Unique): The generated short key.
  - `short_url` (String, Unique): The full short URL.
  - `long_url` (String, Not Null): The original long URL.

### **3. Architecture**
- **Framework**: FastAPI for building web APIs.
- **Folder Structure**:
  ```plaintext
  app/
  ├── main.py              # Entry point for the application
  ├── routers/             # API route handlers
  ├── schemas/             # Pydantic models for request/response validation
  ├── models/              # SQLAlchemy models for database tables
  ├── crud/                # CRUD operations for database interactions
  ├── dependencies/        # Shared dependencies (e.g., database sessions)
  ├── utils/               # Helper utilities (e.g., shortener algorithm, error handling)
  └── db.py                # Database configuration and initialization
  ```

---

## **Endpoints**

### **1. Create Short URL**
**Endpoint**: `POST /`

- **Description**: Generate a short URL for a given long URL.
- **Method**: `POST`

#### **Request Body**
```json
{
    "url": "https://example.com"
}
```

#### **Response**
```json
{
    "msg": "Successfully Added to DB",
    "key": "abc1234",
    "short_url": "https://short.ly/abc1234",
    "long_url": "https://example.com"
}
```

#### **Error Responses**
- **500**: Failed to add URL.

#### **Example cURL Command**
```bash
curl -X POST "http://127.0.0.1:8000/" -H "Content-Type: application/json" -d '{"url":"https://example.com"}'
```

---

### **2. Redirect to Long URL**
**Endpoint**: `GET /{key}`

- **Description**: Redirects a short URL key to its corresponding long URL.
- **Method**: `GET`

#### **Path Parameter**
- `key`: The short URL key (e.g., `abc1234`).

#### **Response**
Redirects to the corresponding long URL with status code `302`.

#### **Error Responses**
- **404**: Short URL does not exist.

#### **Example**
```bash
curl -X GET "http://127.0.0.1:8000/abc1234"
```

---

### **3. Delete URL**
**Endpoint**: `DELETE /{key_or_url}`

- **Description**: Deletes a short URL entry based on its key or long URL.
- **Method**: `DELETE`

#### **Path Parameter**
- `key_or_url`: The short URL key (e.g., `abc1234`) or the long URL.

#### **Response**
```json
{
    "message": "Successfully deleted the URL from the database"
}
```

#### **Error Responses**
- **404**: URL does not exist; nothing to delete.

#### **Example cURL Command**
```bash
curl -X DELETE "http://127.0.0.1:8000/abc1234"
```

---

## **Testing**

### **1. Using Swagger UI**
- Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- Test each endpoint interactively by providing inputs and checking outputs.

### **2. Using Postman**
1. Import the following example requests:
   - **Create Short URL**:
     - URL: `POST http://127.0.0.1:8000/`
     - Body:
       ```json
       {
           "url": "https://example.com"
       }
       ```
   - **Redirect to Long URL**:
     - URL: `GET http://127.0.0.1:8000/abc1234`
   - **Delete URL**:
     - URL: `DELETE http://127.0.0.1:8000/abc1234`
2. Verify responses.

### **3. Using cURL**
Use the example cURL commands provided above for each endpoint.

---

## **Error Handling**
The API returns structured error responses:

- **404 Not Found**:
  ```json
  {
      "detail": {
          "message": "This short URL does not exist"
      }
  }
  ```
- **500 Internal Server Error**:
  ```json
  {
      "detail": "Failed to add URL"
  }
  ```

---

## **Notes**

1. **Realistic URL Shortener Behavior**:
   - Short URLs are resolved directly at the root path (`/{key}`).
   - Public API only includes the `POST /` endpoint for generating short URLs.
2. **Security**:
   - Consider adding authentication for sensitive endpoints in production environments.

---

This documentation should provide everything needed to interact with and test the URL Shortener API effectively.

