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

## Testing & Debugging

I add a dedicated section describing how I test and debug the application locally.

### run_server.py (debug runner)

I create `run_server.py` which starts the FastAPI app via `uvicorn` with reload enabled. I run the server with:

```powershell
python run_server.py
```

This runner makes it easy for me to use `breakpoint()` in the code or attach an IDE debugger. I can also run with the Python debugger:

```powershell
python -m pdb run_server.py
```

### Logging

I configure application-level logging using Python's `logging` module (see `app/core/security.py` and other modules). I use structured log messages to help trace events and errors.

### Sentry (optional)

I mention Sentry as an optional monitoring tool. To enable Sentry in production or staging, I install `sentry-sdk` and initialize it in `main.py` with the DSN from the Sentry project settings. I do not enable Sentry by default in this repository.

### Tests

I use `pytest` together with `httpx` to run unit and integration tests. The tests create a temporary SQLite test database (`tests/test.db`) and automatically create/drop tables via the test fixtures. To run tests:

```powershell
pytest -q
```

If tests show database/table errors, I verify filesystem permissions and that the test fixtures create tables before the TestClient starts.

### Performance testing (outline)

For load testing I recommend `locust` or tools like `k6` for more advanced scenarios. I do not include load tests in this repository by default.

### Quick review checklist after edits

After I make code or dependency changes I do the following checks:

- Run `pytest` and fix failing tests.
- Start the app with `python run_server.py` and exercise endpoints in `/docs`.
- Verify file upload/download behavior (uploads saved to `uploads/`, downloads return `Content-Disposition: attachment`).
- Check logs for errors and stack traces.
