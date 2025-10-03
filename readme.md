## Project: Advanced Data Management in FastAPI (SQLite)

This repository is a focused FastAPI project that uses an async SQLite backend (via `aiosqlite`) and demonstrates common data-management features: async CRUD with SQLAlchemy, JWT auth, file upload/download, and tests.

***

### 🎯 Project Objective (current)

Keep the project simple and reliable by using a single async SQL backend (SQLite) for persistence while demonstrating:

1. Async CRUD with SQLAlchemy + aiosqlite.
2. Secure user authentication (JWT + password hashing).
3. File upload and download endpoints with proper download behavior.
4. Automated tests that run against a disposable test database.

***

### 🧱 Architectural Components & Tasks

I will achieve my objectives by focusing on the following core development tasks, each introducing a critical piece of the data architecture:

| Task Title | Description | Key Technologies & Concepts |
| :--- | :--- | :--- |
| **Setting up SQL databases** | I will configure a relational database connection and set up the initial schema (tables and models) for my application. | **SQLAlchemy** (ORM), Database Configuration, Connection Pooling. |
| **Understanding CRUD operations with SQLAlchemy** | I'll write the business logic to **Create, Read, Update, and Delete** records using SQLAlchemy's ORM within my FastAPI routes. | SQLAlchemy Session Management, ORM Queries, Dependency Injection. |
| **Integrating NoSQL (optional)** | There is no active MongoDB integration in this simplified project. If added later, it would live in a separate module. | (optional) Motor or other NoSQL driver. |
| **Working with data validation and serialization** | I will use **Pydantic** extensively to ensure incoming data meets specific criteria and that my outgoing data is correctly formatted for clients. | Pydantic Models, Schema Definition, Data Type Enforcement. |
| **Working with file uploads and downloads** | I will implement endpoints that can accept files (e.g., images, documents) from a client and endpoints that allow clients to download stored files. | FastAPI `File` and `UploadFile`, Streaming Responses, I/O Handling. |
| **Handling asynchronous data operations** | I will ensure all my database interactions are non-blocking by using **`async/await`** with the appropriate async database drivers. | **`async`** Functions, Non-blocking I/O, Performance Optimization. |
| **Securing sensitive data and best practices** | I'll focus on methods like hashing passwords and environment variable management to protect sensitive information in my application and database. | Hashing Libraries (e.g., `passlib`), Environment Variables, Security Best Practices. |

***

### 🛠️ Key Dependencies I'll Be Using

To complete this project, I'll be integrating several high-performance libraries into my FastAPI environment:

| Dependency | Purpose in this Project |
| :--- | :--- |
| `sqlalchemy` | The main **SQL Object-Relational Mapper** for database interaction. |
| `aiosqlite` | The async SQLite driver used by this project for non-blocking DB operations. |
| `python-multipart` | The library FastAPI uses internally to handle **file uploads**. |
| `passlib` | Essential for **hashing and verifying passwords** and other sensitive data. |

***

### ⚙️ Demo & Testing Strategy

Focus on correctness and simple reproducibility with SQLite and the included tests:

1. Database Connection: tests and startup logic create the SQLite schema automatically (see `app/config/database.py`).
2. CRUD Functionality: use the interactive docs (`/docs`) to exercise CRUD endpoints for Users and Items.
3. File Testing: upload a file via POST `/upload/` and download via GET `/download/{filename}` — download responses are set with `Content-Disposition: attachment` so the browser will save the file.
4. Error Handling: use Swagger to submit malformed payloads to see 422 responses from Pydantic validation.
5. Tests: run `pytest -q` to run the integrated test suite which uses a temporary test database.
