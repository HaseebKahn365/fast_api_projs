from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import mimetypes
from ..routers.auth import get_current_user

router = APIRouter()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", "uploads")

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "File uploaded successfully"}

@router.get("/download/{filename}")
async def download_file(filename: str, current_user = Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Guess media type; default to binary to force download when appropriate
    media_type, _ = mimetypes.guess_type(file_path)
    if media_type is None:
        media_type = "application/octet-stream"

    # Set Content-Disposition to attachment so the browser downloads the file
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return FileResponse(path=file_path, media_type=media_type, headers=headers)