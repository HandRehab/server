import logging
from fastapi import APIRouter
from games.box.main import box_play
from db import get_db
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
db=get_db()
app = APIRouter(tags=["box"])

class UsernameRequest(BaseModel):
    username: str

@app.post("/play", operation_id="play_game")
async def handle_play(username_request: UsernameRequest):
    username = username_request.username #fetch username from frontend
    logger.info("Handling play_game request")
    try:
        await box_play()
        result=box_play()
        print(result)
        return {"message": "Playing game"}
    except Exception as e:
        logger.exception("An error occurred while playing the game:")
        return {"error": str(e)}
    #user= await db["users"].find_one({"username":username})
    #print(result)

@app.post("/notFound", operation_id="not_found")
async def handle_not_found():
    logger.info("Handling not_found request")
    return {"message": "Not found"}
