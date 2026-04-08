from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class ShortenURLRequest(BaseModel):
    long_url: HttpUrl
    expires_at: Optional[datetime] = None


class ShortenURLResponse(BaseModel):
    short_url: str
