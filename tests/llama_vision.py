import requests
import base64
import json

def test_llama_vision_api(image_path, prompt, api_endpoint="http://localhost:8000/vision"):
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # Send POST request to Llama-Vision
    payload = {
        "image": encoded_image,
        "prompt": prompt
    }
    response = requests.post(api_endpoint, json=payload)
    
    if response.ok:
        print("Response from Llama-Vision:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    # Replace with the name of the JPEG file in your current directory
    test_image = "test_image.jpg"
    user_prompt = "You are an assistive navigation guide for visually impaired users. Look at the image and provide a brief, clear description in one sentence (or two bullet points) that includes only essential information for safe navigation (key landmarks, obstacles, and directional cues). Use no more than 30 words and avoid extraneous details. If the image is unclear, provide your best interpretation without speculation."
    test_llama_vision_api(test_image, user_prompt)