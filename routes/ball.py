import logging
import time
from fastapi import APIRouter
from games.catch_ball.catch_ball import start_ball

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = APIRouter(tags=["ball"])

# Initialize Clock for FPS
fps = 30

@app.post("/play4", operation_id="play_game4")
async def handle_play4():
    logger.info("Handling play_game request")
    try:
        score = await start_ball()
        return score
    except Exception as e:
        logger.exception("An error occurred while playing the game:")
        return {"error": str(e)}

@app.post("/notFound", operation_id="not_found")
async def handle_not_found():
    logger.info("Handling not_found request")
    return {"message": "Not found"}
