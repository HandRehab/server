from fastapi import APIRouter
from bson import ObjectId
from db import get_db
from schemas import createMessageBody


app = APIRouter(
    tags=["message"]
)

db = get_db()

@app.post('/message')
async def message_user(body: createMessageBody):
    #defaul message body
    user_message={
        "username":"",
        "message":"",
        "timestamp":""
    }
    #update function 
    user_message.update({
        "username": body.username,
        "message": body.message,
        "timestamp": body.timestamp
    })

    try:
        result = await db["msg"].insert_one(user_message)
        if result.inserted_id:
            return {"message": "User Message sent successfully", "success": True}
        else:
            return {"message": "Error sending message user", "success": False}
    except Exception as e:
        {"message": f"Error sending message to user: {str(e)}", "success": False}
            

