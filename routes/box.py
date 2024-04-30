import logging
from fastapi import APIRouter
from games.box.main import box_play
from db import get_db
from pydantic import BaseModel
from datetime import datetime
from schemas import createUserBody



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
db=get_db()
app = APIRouter(tags=["box"])

class BoxData(BaseModel):
    score: int
class UsernameRequest(BaseModel):
    username: str

@app.post("/play", operation_id="play_game")
async def handle_play(username_request: UsernameRequest, box_data: BoxData):
    username = username_request.username #fetch username from frontend
    logger.info("Handling play_game request")
    try:
        
        res= await box_play() #to maybe show from the game
        score = box_data.score #to take from fastAPI docs

        #print(res)
        
        timestamp = datetime.now().strftime("%d-%m-%Y")
        
        user= await db["users"].find_one({"username":username})
        if user:
            filter_criteria = {"username": username}
        # Update balloon data with timestamp and score
            update_operation = {"$set": {"box." + timestamp: score}}
            await db["users"].update_one(filter_criteria, update_operation)
        return {"message": "Box data updated successfully"}
    except Exception as e:
        logger.exception("An error occurred while playing the game:")
        return {"error": str(e)}
    
    #print(result)

@app.post("/notFound", operation_id="not_found")
async def handle_not_found():
    logger.info("Handling not_found request")
    return {"message": "Not found"}
