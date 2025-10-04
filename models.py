from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    username: str
    message: str
    timestamp: str

class FileUploadResponse(BaseModel):
    filename: str
    download_url: str
    

class HistoryResponse(BaseModel):
    messages: list[Message]