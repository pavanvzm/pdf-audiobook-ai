# PDF to Audiobook AI Voice Agent

An intelligent AI voice agent that converts PDFs into high-quality audiobooks with voice cloning, smart summarization, and natural speech synthesis using Chatterbox TTS.

## 🚀 Features

- **PDF Text Extraction**: Advanced OCR and text extraction from PDFs.
- **Smart Summarization**: LLM-powered intelligent content summarization.
- **Voice Cloning**: Custom voice training and cloning capabilities (Placeholder).
- **High-Quality TTS**: Chatterbox-based text-to-speech synthesis (Placeholder).
- **Batch Processing**: Handle multiple PDFs efficiently via a web interface.
- **Audio Export**: Multiple audio format support (MP3, WAV, M4A).
- **Web Interface**: User-friendly web UI for easy interaction.

## 🏗️ Architecture

The project is structured as a Flask web application with a Celery worker for background processing.

- **`web_interface/`**: Contains the Flask application, routes, and templates.
- **`src/`**: Contains the core application logic.
  - **`pdf_processor/`**: Handles PDF text extraction.
  - **`summarization/`**: Manages text summarization with LLMs.
  - **`tts_engine/`**: A placeholder for the Text-to-Speech engine.
  - **`voice_cloning/`**: A placeholder for the voice cloning module.
- **`scripts/`**: Contains utility scripts for tasks like downloading models or training voices.
- **`tests/`**: Contains the test suite.

## 📋 Requirements

- Python 3.8+
- Redis
- Tesseract OCR
- FFmpeg

## 🛠️ Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd pdf-audiobook-ai
    ```

2.  **Install System Dependencies**
    - **Redis**: Follow the official installation instructions for your OS: [https://redis.io/docs/getting-started/](https://redis.io/docs/getting-started/)
    - **Tesseract & FFmpeg**:
      ```bash
      # Ubuntu/Debian
      sudo apt-get update
      sudo apt-get install tesseract-ocr ffmpeg

      # macOS
      brew install tesseract ffmpeg
      ```

3.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **Create a `.env` file** from the example:
    ```bash
    cp .env.example .env
    ```
2.  **Edit the `.env` file** with your settings, especially your `OPENAI_API_KEY`.

3.  **Create a `config.yaml` file** from the example:
    ```bash
    cp config/config.example.yaml config/config.yaml
    ```
4.  **Edit `config/config.yaml`** to customize application settings.

## 🏃‍♀️ Running the Application

This application requires two main processes to be running: the Flask web server and the Celery worker.

1.  **Start Redis Server**
    If you installed Redis locally, ensure it is running.
    ```bash
    redis-server
    ```

2.  **Start the Celery Worker**
    In a new terminal, navigate to the project root and run:
    ```bash
    celery -A web_interface.app.celery worker --loglevel=info
    ```

3.  **Start the Flask Web Server**
    In another terminal, run the Flask application:
    ```bash
    python web_interface/app.py
    ```

4.  **Access the Web Interface**
    Open your browser and navigate to `http://localhost:8000`.

## 🎯 Usage

-   Open the web interface in your browser.
-   Select a PDF file to upload.
-   Choose your desired conversion options.
-   Click "Convert to Audiobook".
-   The conversion will be processed in the background. The status will be updated on the page.
-   Once complete, a download link for the audiobook will appear.
