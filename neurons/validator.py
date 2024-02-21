# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# (developer): ETG Team
# Copyright © 2023 <ETG>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# import os
# import sys
# import asyncio

# # Set the project root path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# # Set the 'AudioSubnet' directory path
# audio_subnet_path = os.path.abspath(project_root)

# # Add the project root and 'AudioSubnet' directories to sys.path
# sys.path.insert(0, project_root)
# sys.path.insert(0, audio_subnet_path)

# from classes.tts import TextToSpeechService 
# from classes.vc import VoiceCloningService
# from classes.ttm import MusicGenerationService

# async def main():
#     services = [
#         MusicGenerationService(),
#         TextToSpeechService(),
#         VoiceCloningService(),
#     ]

#     # Initialize an empty list to hold our tasks
#     tasks = []

#     # Iterate through each service and create an asynchronous task for its run_async method
#     for service in services:
#         if isinstance(service, TextToSpeechService):
#             service.new_wandb_run()  # Initialize the Weights & Biases run if the service is TextToSpeechService
#         task = asyncio.create_task(service.run_async())
#         tasks.append(task)

#         await asyncio.sleep(0.1)  # Short delay between task initializations if needed

#     # Wait for all tasks to complete
#     await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())















import os
import sys
import uvicorn
import asyncio
import requests
import nest_asyncio
from pyngrok import ngrok
import concurrent.futures
from fastapi import FastAPI
from multiprocessing import Process

# Set the project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(_file_), ".."))
# Set the 'AudioSubnet' directory path
audio_subnet_path = os.path.abspath(project_root)

# Add the project root and 'AudioSubnet' directories to sys.path
sys.path.insert(0, project_root)
sys.path.insert(0, audio_subnet_path)

# Assuming the classes are defined in these modules
from classes.tts import TextToSpeechService, AIModelService
from classes.vc import VoiceCloningService

from fastapi import FastAPI
import uvicorn
from pyngrok import ngrok

# Define your FastAPI app
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Define Server Management Class
class FastAPIServer:
    def _init_(self, fastapi_app: FastAPI):
        self.fastapi_app = fastapi_app

    async def run_async(self):
        # Setup ngrok tunnel
        ngrok_tunnel = ngrok.connect(8000)
        print('Public URL:', ngrok_tunnel.public_url)
        # Run the server using uvicorn
        config = uvicorn.Config(app=self.fastapi_app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()


        
import asyncio
from classes.tts import TextToSpeechService, AIModelService
from classes.vc import VoiceCloningService
from app import FastApiServer

# Ensure the below imports are correct based on your directory structure and file names
# from your_base_class_or_module import FastAPIServer, app

async def main():
    # Initialize all services
    #fastapi_server = FastAPIServer(app)
    AIModelService()
    tts_service = TextToSpeechService()
    vc_service = VoiceCloningService()
    fastapi_server = FastAPIServer(app)

    # Prepare tasks for all services
    vc_task = asyncio.create_task(vc_service.run_async())
    tts_task = asyncio.create_task(tts_service.run_async())
    fastapi_task = asyncio.create_task(fastapi_server.run_async())

    # Wait for all tasks to complete
    await asyncio.gather(vc_task, tts_task,fastapi_task)

if _name_ == "_main_":
    asyncio.run(main())







