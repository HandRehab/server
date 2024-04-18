from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from games.BalloonPop.BalloonPop import start_balloon
import threading
from queue import Queue
import os
from fastapi import APIRouter

app = APIRouter(
    tags=["balloon"]
)


@app.get("/hi")
async def main():
    # print(os.environ['VIRTUAL_ENV'])
        result_queue = Queue()
        user_name = "Player1"

        game_thread = threading.Thread(target=start_balloon, args=(result_queue,))
        game_thread.start()

        # Wait for the thread to finish
        game_thread.join()

        # Retrieve the result from the queue
        result = result_queue.get()
        print(result)

        if(result["status"] == "Game over"):
            data = {
                "username": user_name,
                "score": result["score"]
            }
            print("DATA===", data)
            # Sample code to insert to mongodb
            # result = collection.insert_one(data)

        return {"message": "msg"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from uvicorn.reloaders.statreload import StatReload
# from uvicorn.main import run, get_logger
# reloader = StatReload(get_logger(run_config['log_level']))
# reloader.run(run, {
#     'app': app,
#     'host': run_config['api_host'],
#     'port': run_config['api_port'],
#     'log_level': run_config['log_level'],
#     'debug': 'true'
# })