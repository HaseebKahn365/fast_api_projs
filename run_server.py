import uvicorn

# Simple runner script to start the FastAPI app in a way that's convenient for
# debugging (breakpoints, IDE attach, pdb). The project entrypoint is the
# top-level `main.py` which defines `app`.
try:
    # Prefer importing the app from main.py in project root
    from main import app
except Exception:
    # Fallback: try to import from app.main if project is packaged differently
    from app.main import app


if __name__ == "__main__":
    # Use reload=True for development convenience. Remove in production.
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
