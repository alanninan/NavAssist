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
        
        # Forward to Llama-Vision server (Ollama) with a prompt
        response = requests.post(
            LLAMA_VISION_URL,
            json={"image": image_data, "prompt": PROMPT}
        )
        result = response.json().get("text", "No response.")
        
        await websocket.send(result)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Runs forever

asyncio.run(main())