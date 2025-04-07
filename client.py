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
import pyttsx3
import os
from picamera2 import Picamera2
import time

# WebSocket server URI (replace <nvidia-server-ip> with the actual IP address)
SERVER_URI = "ws://<nvidia-server-ip>:8765"

# Function to initialize Picamera2 and return the instance
def init_camera():
    picam2 = Picamera2()
    # Create a video configuration for continuous capture (adjust resolution if needed)
    config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()
    # Allow camera to warm up a bit
    time.sleep(0.2)
    return picam2

# Asynchronous function to capture frames using Picamera2 and send them via WebSocket
async def send_frames():
    # Initialize Picamera2
    picam2 = init_camera()
    async with websockets.connect(SERVER_URI) as ws:
        try:
            while True:
                # Capture a frame as a NumPy array (in RGB format)
                frame_rgb = picam2.capture_array()
                # Convert RGB (Picamera2 default) to BGR (OpenCV default)
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                # Encode the frame as JPEG
                ret, buffer = cv2.imencode('.jpg', frame_bgr)
                if not ret:
                    print("Failed to encode frame.")
                    break

                # Convert JPEG buffer to Base64 string
                encoded = base64.b64encode(buffer).decode('utf-8')
                # Send the encoded frame to the server via WebSocket
                await ws.send(json.dumps({"frame": encoded}))

                # Receive the response from the server
                response = await ws.recv()
                print("LLM response:", response)

                # Convert the response text to speech and play it
                engine = pyttsx3.init()
                engine.say(response)
                engine.runAndWait()

                # Wait for 1 second before capturing the next frame
                await asyncio.sleep(1)
        finally:
            picam2.stop()

# Run the asynchronous function
asyncio.run(send_frames())
