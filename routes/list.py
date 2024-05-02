from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from bson.json_util import dumps
from db import get_db

db = get_db()
app = APIRouter(tags=["list"])
collection = db["users"]

@app.get("/users/{doctorid}")
async def get_users_by_doctor_id(doctorid: int):
    # Define the projection to include only the specified fields
    projection = {"username": 1, "phone": 1, "balloon": 1,  "box": 1,  "_id": 0}
    
    # Query MongoDB to find users with the specified doctor id and userRole value of 2
    users = await collection.find({"doctorid": doctorid, "userRole": 2}, projection).to_list(length=None)
    
    # Convert MongoDB documents to JSON format
    users_json = dumps(users)
    
    return users_json
