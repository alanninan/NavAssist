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

import requests
import base64
import json

def test_llm_api(image_path, prompt, api_endpoint="http://localhost:11434/api/chat"):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # Send POST request to Llama-Vision
    payload = {
        "model": "llava:7b",
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image]
            }
        ]
    }
    response = requests.post(api_endpoint, json=payload)
    
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

if __name__ == "__main__":
    # Replace with the name of the JPEG file in your current directory
    test_image = "test_image.jpg"
    user_prompt = "You are an assistive navigation guide for visually impaired users. Look at the image and provide a brief, clear description in one sentence (or two bullet points) that includes only essential information for safe navigation (key landmarks, obstacles, and directional cues). Use no more than 30 words and avoid extraneous details. If the image is unclear, provide your best interpretation without speculation."
    test_llm_api(test_image, user_prompt)