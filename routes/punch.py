import logging
import time
from fastapi import APIRouter
from games.Punch_game.punch_game import start_punch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(tags=["punch"])

# Initialize Clock for FPS
fps = 30

@app.post("/play6", operation_id="play_game6")
async def handle_play6():
    logger.info("Handling play_game request")
    try:
        score = start_punch()
        return score
    except Exception as e:
        logger.exception("An error occurred while playing the game:")
        return {"error": str(e)}

@app.post("/notFound", operation_id="not_found")
async def handle_not_found():
    logger.info("Handling not_found request")
    return {"message": "Not found"}
