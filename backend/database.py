from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME= os.getenv("DATABASE_NAME")
MONGODB_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]

url_collection = database["urls"]