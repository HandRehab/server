from fastapi import APIRouter
from db import get_db

app = APIRouter(tags=["authentication"])
db = get_db()

@app.get("/validate")
async def validate_user(username: str, password: str):
    user = await db["users"].find_one({"username": username})

    if user:
        if user["password"] == password:
            if user.get("userRole") == 1:
                doctorid = user.get("doctorid")
                return {"message": "Success", "access": True, "userRole": user["userRole"], "doctorid": doctorid}
            else:
                return {"message": "Success", "access": True, "userRole": user["userRole"],"name":user["name"]}
        else:
            return {"message": f"Password for {username} is wrong", "access": False}
    else:
        return {"message": "User not found", "access": False}
