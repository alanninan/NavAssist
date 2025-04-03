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

import time
import cv2
import base64
import json
import requests
from picamera2 import Picamera2

def test_llama_vision_api(prompt, api_endpoint="http://localhost:8000/vision"):
    # Initialize Picamera2 and configure for still capture
    picam2 = Picamera2()
    config = picam2.create_still_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()
    time.sleep(0.2)  # allow the camera to warm up
    
    # Capture an image as a NumPy array (in RGB format)
    image_rgb = picam2.capture_array()
    picam2.stop()
    
    # Convert the image to BGR (as OpenCV uses BGR by default) for JPEG encoding
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    # Encode the image to JPEG format
    ret, buffer = cv2.imencode('.jpg', image_bgr)
    if not ret:
        print("Failed to encode image")
        return
    
    # Base64 encode the JPEG bytes
    encoded_image = base64.b64encode(buffer).decode("utf-8")
    
    # Create the payload with the encoded image and prompt
    payload = {
        "model": "llama3.2-vision",
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image]
            }
        ]
    }
    
    # Send POST request to Llama‑Vision API
    response = requests.post(api_endpoint, json=payload)
    
    if response.ok:
        print("Response from Llama-Vision:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    user_prompt = "You are an assistive navigation guide for visually impaired users. Look at the image and provide a brief, clear description in one sentence (or two bullet points) that includes only essential information for safe navigation (key landmarks, obstacles, and directional cues). Use no more than 30 words and avoid extraneous details. If the image is unclear, provide your best interpretation without speculation."

    test_llama_vision_api(user_prompt)
