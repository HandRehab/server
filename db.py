from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
client=AsyncIOMotorClient("mongodb+srv://admin:admin123@cluster0.5r31v6f.mongodb.net/?retryWrites=true&w=majority")
db = client["handrehab"]
print("Database connection established")

def get_db():
    return db