# Copyright 2025 Alan Ninan Thomas, Milen Shoji, and Sreyas Saji.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import websockets
import requests
import json
import base64

LLAMA_VISION_URL = "http://localhost:8000/vision"
PROMPT = "You are an assistive navigation guide for visually impaired users. Look at the image and provide a brief, clear description in one sentence (or two bullet points) that includes only essential information for safe navigation (key landmarks, obstacles, and directional cues). Use no more than 30 words and avoid extraneous details. If the image is unclear, provide your best interpretation without speculation."

async def handler(websocket, _):
    async for message in websocket:
        data = json.loads(message)
        image_data = data.get("frame", "")
        
        # Prepare the payload to match the cURL example
        payload = {
            "model": "llama3.2-vision",
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT,
                    "images": [image_data]
                }
            ]
        }

        # Send the request to the Llama-Vision server using the updated payload
        response = requests.post(LLAMA_VISION_URL, json=payload)
        result = response_data.get("response", "No response.")

        # Forward the result to the Raspberry Pi
        await websocket.send(result)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Runs forever

asyncio.run(main())