import logging
from fastapi import APIRouter
from games.box.main import box_play

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(tags=["box"])

@app.post("/play", operation_id="play_game")
async def handle_play():
    logger.info("Handling play_game request")
    try:
        await box_play()
        return {"message": "Playing game"}
    except Exception as e:
        logger.exception("An error occurred while playing the game:")
        return {"error": str(e)}

@app.post("/notFound", operation_id="not_found")
async def handle_not_found():
    logger.info("Handling not_found request")
    return {"message": "Not found"}
