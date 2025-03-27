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
import cv2
import base64
import json
from gtts import gTTS
import os

# WebSocket server URI (replace <nvidia-server-ip> with the actual IP address)
SERVER_URI = "ws://<nvidia-server-ip>:8765"

# Function to capture frames from the camera and send them to the server
async def send_frames():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    async with websockets.connect(SERVER_URI) as ws:
        while True:
            # Capture a frame from the camera
            ret, frame = cap.read()
            if not ret:
                print("No frame captured.")
                break

            # Encode the frame as JPEG and convert it to Base64
            _, buffer = cv2.imencode('.jpg', frame)
            encoded = base64.b64encode(buffer).decode('utf-8')

            # Send the encoded frame to the server via WebSocket
            await ws.send(json.dumps({"frame": encoded}))

            # Receive the response from the server
            response = await ws.recv()
            print("LLM response:", response)

            # Convert the response text to speech and play it
            speech = gTTS(text=response, lang='en')
            speech.save("out.mp3")
            os.system("mpg321 out.mp3")  # Adjust for your environment

            # Wait for 1 second before capturing the next frame
            await asyncio.sleep(1)
    # Release the camera resource
    cap.release()

# Run the asynchronous function
asyncio.run(send_frames())