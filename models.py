from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ScrapeRequest(BaseModel):
    url: HttpUrl

class ScrapeResult(BaseModel):
    url: HttpUrl
    title: str
    headings: List[str]
    images: List[str]
    summary: str
    sentiment: str
