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

LLM_API_URL = "http://localhost:11434/api/chat"
PROMPT = "You are an assistive navigation guide for visually impaired users. Look at the image and provide a brief, clear description in one sentence that includes only essential information for safe navigation (key landmarks, obstacles, and directional cues; no colors). Use no more than 30 words, avoid extraneous details and do not call it an image - talk of the image as if it is in front of the user. If the image is unclear, provide your best interpretation without speculation."

async def handler(websocket):
    async for message in websocket:
        data = json.loads(message)
        image_data = data.get("frame", "")
        
        # Prepare the payload to match the cURL example
        payload = {
            "model": "llava:7b",
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT,
                    "images": [image_data]
                }
            ]
        }

        # Send the request to the LLM server using the updated payload
        response = requests.post(LLM_API_URL, json=payload)
        if response.ok:
            full_content = ""
            for line in response.text.splitlines():
                try:
                    data = json.loads(line)
                    full_content += data["message"]["content"]
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {line}")
                except KeyError:
                    print(f"Skipping line due to missing key: {line}")
            print(full_content)
        else:
            print("Error:", response.status_code, response.text)

        # Forward the result to the Raspberry Pi
        await websocket.send(full_content)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Runs forever

asyncio.run(main())