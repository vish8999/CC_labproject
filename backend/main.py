from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from backend.models import ShortenURLRequest, ShortenURLResponse
from backend.database import url_collection
import random
import string
from datetime import datetime,timezone

import os
from dotenv import load_dotenv




app = FastAPI()


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.post("/shorten", response_model=ShortenURLResponse)
async def create_short_url(request: ShortenURLRequest):
    short_code = generate_short_code()
    # url_store[short_code] = str(request.long_url)
    
    document = {
        "short_code": short_code,
        "long_url": str(request.long_url),
        "created_at": datetime.now(timezone.utc),
        "expires_at": request.expires_at,
        "clicks": 0
    }
    
    await url_collection.insert_one(document)
    

    return {
    "short_url": f"{BASE_URL}/{short_code}"
    }


@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    
    document =await url_collection.find_one({
        "short_code":short_code
    })
    
    if not document:
        raise HTTPException(status_code=404, detail="Not found")

    return RedirectResponse(
        url=document["long_url"],
        status_code=302
    )
