# NavAssist — Assistive Navigation System for Visually Impaired Users

## Overview
This project provides an assistive navigation solution for visually impaired individuals using a Raspberry Pi and a remote processing server. It captures real-time video, processes it with an AI model, and converts the extracted information into auditory feedback to help users navigate safely.

## Features
- **Real-time Video Capture:** Raspberry Pi camera captures live footage.
- **WebSocket Communication:** Frames are sent to a remote processing server for analysis.
- **AI-Based Image Analysis:** Uses an AI model to analyze images and extract key navigation cues.
- **Text-to-Speech Conversion:** Converts AI-generated text responses into speech for the user.
- **Low Latency Processing:** Optimized for near real-time feedback.

## System Architecture
1. **Raspberry Pi Client**
   - Captures video frames using OpenCV.
   - Encodes and transmits frames to the remote processing server via WebSockets.
   - Receives textual descriptions and converts them into speech.
   
2. **Remote Processing Server**
   - Hosts the AI model for image processing.
   - Receives image frames and extracts navigation-relevant information.
   - Sends back concise descriptions for auditory feedback.

## Installation & Setup
### Prerequisites
- Raspberry Pi with a camera module.
- A server with an AI model (Llama-Vision or equivalent).
- Python 3.x installed on both devices.
- Required Python libraries:
  ```sh
  pip install -r requirements.txt
  ```
- `mpg321` installed for audio playback on Raspberry Pi:
  ```sh
  sudo apt-get install mpg321
  ```

### Running the Raspberry Pi Client
1. Update the `SERVER_URI` in `client.py` with your processing server's IP.
2. Run the client script:
   ```sh
   python client.py
   ```

### Running the Processing Server
1. Ensure the AI model API (Llama-Vision) is running.
2. Start the WebSocket server:
   ```sh
   python server.py
   ```

## Usage
1. The Raspberry Pi captures and sends video frames to the processing server.
2. The processing server analyzes the frames and returns navigation cues.
3. The Raspberry Pi converts the response into speech and plays it through earphones.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Meta's Llama 3.2 Vision.
- OpenCV and gTTS for video processing and speech synthesis.

## Contribution
Contributions are welcome! Feel free to fork this repository and submit pull requests with improvements or bug fixes.

