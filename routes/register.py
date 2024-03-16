from fastapi import APIRouter
from bson import ObjectId
from db import get_db
from schemas import createUserBody

app = APIRouter(
    tags=["register"]
)

db = get_db()

@app.post("/register")
async def create_user(body: createUserBody):
    # Check if a user with the same username already exists
    existing_user = await db["users"].find_one({"username": body.username})
    if existing_user:
        return {"message": "Username already exists", "success": False}
    
    user_data = {
        "adminid": "athul",
        "doctorid": body.doctorid,
    }
    
    if body.userRole == 1:
        user_data.update({
            "username": body.username,
            "name": body.name,
            "phone": body.phone,
            "password": body.password,
            "doctorid": body.doctorid,
            "adminid": body.adminid,
            "userRole": body.userRole,
        })
    elif body.userRole == 2:
        user_data.update({
            "username": body.username,
            "name": body.name,
            "phone": body.phone,
            "password": body.password,
            "birthdate": body.birthdate,
            "gender": body.gender,
            "doctorid": body.doctorid,
            "userRole": body.userRole
        })
        
    try:
        result = await db["users"].insert_one(user_data)
        if result.inserted_id:
            return {"message": "User created successfully", "success": True}
        else:
            return {"message": "Error creating user", "success": False}
    except Exception as e:
        return {"message": f"Error creating user: {str(e)}", "success": False}
