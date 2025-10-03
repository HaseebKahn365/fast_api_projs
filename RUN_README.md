# Advanced Data Management in FastAPI

This is a simplified FastAPI project demonstrating advanced data management with SQLite database.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. The database will be automatically created as `app.db` in the project root.

## Run the Application

```
python main.py
```

Or with uvicorn:
```
uvicorn main:app --reload
```

## Run Tests

```
pytest
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Features

- ✅ SQLite database integration with SQLAlchemy
- ✅ User authentication with JWT tokens
- ✅ CRUD operations for items
- ✅ File upload and download
- ✅ Data validation with Pydantic
- ✅ Password hashing with passlib
- ✅ Async database operations
- ✅ Comprehensive test suite