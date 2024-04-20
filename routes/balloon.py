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

app = APIRouter(
    tags=["balloon"]
)
db=get_db()

class UsernameRequest(BaseModel):
    username: str

@app.post("/balloon")
async def main(username_request: UsernameRequest):
        username = username_request.username
        
        
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

        
        user= await db["users"].find_one({"username":username})
        if user:
            filter_criteria = {"username": username}
            new_balloon_value = result["score"] 
            update_operation = {"$set": {"balloon": new_balloon_value}}
            res=await db["users"].update_one(filter_criteria, update_operation)
        data = {
                "username": user_name,
                "baloon": result["score"]
            }
        print("DATA===", data)
        print(username)
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