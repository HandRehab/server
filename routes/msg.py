from fastapi import APIRouter
from db import get_db
from pymongo import DESCENDING

app = APIRouter(
    tags=["msg"]
)

db = get_db()

@app.get('/chat/{username}')
async def get_user_messages(username: str):
    try:
        # Query the database to find all messages sent to the specified username
        messages_cursor = db["msg"].find({"username": username}).sort("timestamp", DESCENDING)
        # Extract only the message content from each message and convert to a list
        messages = [message["message"] async for message in messages_cursor]
        print(messages)
        return {"messages": messages}
    except Exception as e:
        return {"error": f"Error retrieving messages for user '{username}': {str(e)}"}
