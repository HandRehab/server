from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from games.BalloonPop.BalloonPop import start_balloon
import threading
from queue import Queue
import os
from fastapi import APIRouter
from db import get_db
from schemas import createUserBody
from pydantic import BaseModel
from datetime import datetime


app = APIRouter(
    tags=["balloon"]
)
db=get_db()



class BalloonData(BaseModel):
    score: int

class UsernameRequest(BaseModel):
    username: str

@app.post("/balloon")
async def main(username_request: UsernameRequest, balloon_data: BalloonData):
    username = username_request.username
    score = balloon_data.score

    # Generate timestamp in the format "dd-mm-yyyy"
    timestamp = datetime.now().strftime("%d-%m-%Y")
    
    result_queue = Queue()
    user_name = "Player1"

    # Start the balloon processing in a separate thread
    game_thread = threading.Thread(target=start_balloon, args=(result_queue,))
    game_thread.start()

    # Wait for the thread to finish
    game_thread.join()

    # Retrieve the result from the queue
    result = result_queue.get()

    # Update user's balloon data
    user = await db["users"].find_one({"username": username})
    if user:
        filter_criteria = {"username": username}
        # Update balloon data with timestamp and score
        update_operation = {"$set": {"balloon." + timestamp: score}}
        await db["users"].update_one(filter_criteria, update_operation)
    
    return {"message": "Balloon data updated successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
