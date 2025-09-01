# PDF to Audiobook AI Voice Agent

An intelligent AI voice agent that converts PDFs into high-quality audiobooks with voice cloning, smart summarization, and natural speech synthesis using Chatterbox TTS.

## 🚀 Features

- **PDF Text Extraction**: Advanced OCR and text extraction from PDFs
- **Smart Summarization**: LLM-powered intelligent content summarization
- **Voice Cloning**: Custom voice training and cloning capabilities
- **High-Quality TTS**: Chatterbox-based text-to-speech synthesis
- **Batch Processing**: Handle multiple PDFs efficiently
- **Audio Export**: Multiple audio format support (MP3, WAV, M4A)
- **Web Interface**: User-friendly web UI for easy interaction

## 🏗️ Architecture

```
├── pdf_processor/          # PDF text extraction and preprocessing
├── voice_cloning/          # Voice training and cloning modules
├── summarization/          # LLM integration for smart summarization
├── tts_engine/            # Chatterbox TTS integration
├── web_interface/         # Flask/FastAPI web application
├── models/               # Trained voice models storage
├── outputs/              # Generated audiobook outputs
└── config/               # Configuration files
```

## 📋 Requirements

### System Requirements
- Python 3.8+
- CUDA-capable GPU (recommended for voice training)
- 8GB+ RAM
- 10GB+ disk space for models

### Dependencies
```bash
# Core dependencies
torch>=1.9.0
torchaudio>=0.9.0
transformers>=4.20.0
openai>=0.27.0
PyPDF2>=2.10.0
pdfplumber>=0.7.0
pytesseract>=0.3.10
librosa>=0.9.0
soundfile>=0.10.0
flask>=2.0.0
fastapi>=0.68.0
uvicorn>=0.15.0
celery>=5.2.0
redis>=4.0.0
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/pdf-audiobook-ai.git
cd pdf-audiobook-ai
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr ffmpeg

# macOS
brew install tesseract ffmpeg

# Windows
# Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 5. Setup Configuration
```bash
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your API keys and settings
```

### 6. Download Base Models
```bash
python scripts/download_models.py
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
REDIS_URL=redis://localhost:6379
MODEL_PATH=./models
OUTPUT_PATH=./outputs
TEMP_PATH=./temp
```

### config.yaml
```yaml
pdf_processing:
  ocr_enabled: true
  languages: ["eng", "spa", "fra"]
  
voice_cloning:
  sample_rate: 22050
  training_epochs: 1000
  batch_size: 32
  
summarization:
  model: "gpt-3.5-turbo"
  max_tokens: 500
  temperature: 0.7
  
tts:
  model_type: "chatterbox"
  speed: 1.0
  pitch: 1.0
```

## 🎯 Usage

### Quick Start
```python
from pdf_audiobook import PDFAudiobookConverter

# Initialize converter
converter = PDFAudiobookConverter()

# Convert PDF to audiobook
audiobook = converter.convert(
    pdf_path="book.pdf",
    voice_model="custom_voice",
    summarize=True,
    output_format="mp3"
)

print(f"Audiobook saved to: {audiobook.output_path}")
```

### Web Interface
```bash
# Start the web server
python app.py

# Access at http://localhost:8000
```

### Voice Cloning Training
```python
from voice_cloning import VoiceTrainer

# Train custom voice
trainer = VoiceTrainer()
trainer.train(
    audio_samples_dir="./voice_samples",
    voice_name="my_voice",
    epochs=1000
)
```

## 📁 Project Structure

```
pdf-audiobook-ai/
│
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── config.yaml
│   └── config.example.yaml
│
├── src/
│   ├── __init__.py
│   ├── pdf_processor/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── preprocessor.py
│   │   └── ocr_handler.py
│   │
│   ├── voice_cloning/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── model.py
│   │   └── data_loader.py
│   │
│   ├── summarization/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── summarizer.py
│   │   └── chunker.py
│   │
│   ├── tts_engine/
│   │   ├── __init__.py
│   │   ├── chatterbox_wrapper.py
│   │   ├── audio_processor.py
│   │   └── voice_manager.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py
│       ├── audio_utils.py
│       └── logging_config.py
│
├── web_interface/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   ├── tasks.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── templates/
│       ├── index.html
│       ├── upload.html
│       └── results.html
│
├── scripts/
│   ├── download_models.py
│   ├── train_voice.py
│   └── batch_convert.py
│
├── tests/
│   ├── __init__.py
│   ├── test_pdf_processor.py
│   ├── test_voice_cloning.py
│   ├── test_summarization.py
│   └── test_tts_engine.py
│
├── models/
│   └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
└── temp/
    └── .gitkeep
```

## 🔧 Core Components

### 1. PDF Processing (src/pdf_processor/)

**extractor.py**
```python
import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

class PDFExtractor:
    def __init__(self, ocr_enabled=True):
        self.ocr_enabled = ocr_enabled
    
    def extract_text(self, pdf_path):
        """Extract text from PDF using multiple methods"""
        text = ""
        
        # Try pdfplumber first (best for text-based PDFs)
        try:
            text = self._extract_with_pdfplumber(pdf_path)
            if len(text.strip()) > 100:
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Fallback to OCR if enabled
        if self.ocr_enabled:
            text = self._extract_with_ocr(pdf_path)
        
        return text
    
    def _extract_with_pdfplumber(self, pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_with_ocr(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # OCR the image
            page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
        
        doc.close()
        return text
```

### 2. Voice Cloning (src/voice_cloning/)

**trainer.py**
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import librosa
import soundfile as sf
from pathlib import Path

class VoiceTrainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def train(self, audio_samples_dir, voice_name, epochs=1000):
        """Train voice cloning model on audio samples"""
        
        # Prepare dataset
        dataset = self._prepare_dataset(audio_samples_dir)
        dataloader = DataLoader(dataset, batch_size=self.config.batch_size, shuffle=True)
        
        # Initialize model (using Chatterbox architecture)
        model = self._initialize_model()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        
        # Training loop
        for epoch in range(epochs):
            total_loss = 0
            for batch in dataloader:
                optimizer.zero_grad()
                
                # Forward pass
                loss = model(batch)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss/len(dataloader)}")
        
        # Save trained model
        self._save_model(model, voice_name)
    
    def _prepare_dataset(self, audio_dir):
        # Implementation for audio preprocessing and dataset creation
        pass
    
    def _initialize_model(self):
        # Initialize Chatterbox-based voice cloning model
        pass
    
    def _save_model(self, model, voice_name):
        model_path = f"models/{voice_name}.pth"
        torch.save(model.state_dict(), model_path)
        print(f"Model saved to {model_path}")
```

### 3. LLM Summarization (src/summarization/)

**summarizer.py**
```python
import openai
from typing import List
import tiktoken

class LLMSummarizer:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)
        
    def summarize_text(self, text: str, summary_type: str = "chapter") -> str:
        """Summarize text using LLM"""
        
        # Chunk text if too long
        chunks = self._chunk_text(text, max_tokens=3000)
        
        if len(chunks) == 1:
            return self._summarize_chunk(chunks[0], summary_type)
        else:
            # Summarize each chunk then create final summary
            chunk_summaries = []
            for chunk in chunks:
                summary = self._summarize_chunk(chunk, "section")
                chunk_summaries.append(summary)
            
            # Create final summary from chunk summaries
            combined = "\n\n".join(chunk_summaries)
            return self._summarize_chunk(combined, summary_type)
    
    def _chunk_text(self, text: str, max_tokens: int = 3000) -> List[str]:
        """Split text into chunks that fit within token limits"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            test_chunk = current_chunk + ". " + sentence if current_chunk else sentence
            
            if len(self.encoding.encode(test_chunk)) <= max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _summarize_chunk(self, text: str, summary_type: str) -> str:
        """Summarize a single chunk of text"""
        
        prompts = {
            "chapter": "Summarize this chapter in a clear, engaging way suitable for audio narration. Focus on key plot points, character development, and important themes:",
            "section": "Provide a concise summary of this text section, highlighting the main ideas and important details:",
            "book": "Create a comprehensive summary of this book content, capturing the essential narrative, themes, and key insights:"
        }
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at creating clear, engaging summaries for audiobook narration."},
                {"role": "user", "content": f"{prompts.get(summary_type, prompts['section'])}\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
```

### 4. TTS Engine (src/tts_engine/)

**chatterbox_wrapper.py**
```python
import torch
import librosa
import soundfile as sf
from pathlib import Path
import numpy as np

class ChatterboxTTS:
    def __init__(self, model_path: str = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path):
        """Load Chatterbox TTS model"""
        # Integration with Chatterbox model
        # This would use the actual Chatterbox implementation
        pass
    
    def synthesize(self, text: str, voice_model: str, output_path: str) -> str:
        """Convert text to speech using specified voice model"""
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        # Generate audio
        audio = self.model.synthesize(
            text=processed_text,
            voice=voice_model,
            sample_rate=22050
        )
        
        # Save audio file
        sf.write(output_path, audio, 22050)
        return output_path
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and prepare text for TTS"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Handle special characters and abbreviations
        replacements = {
            '&': ' and ',
            '@': ' at ',
            '%': ' percent ',
            '$': ' dollars ',
            '#': ' number ',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
```

### 5. Main Application (web_interface/app.py)

**app.py**
```python
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from celery import Celery
import uuid

from src.pdf_processor.extractor import PDFExtractor
from src.summarization.summarizer import LLMSummarizer
from src.tts_engine.chatterbox_wrapper import ChatterboxTTS
from src.voice_cloning.trainer import VoiceTrainer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Celery configuration
celery = Celery(app.name, broker='redis://localhost:6379')

class PDFAudiobookConverter:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.summarizer = LLMSummarizer(api_key=os.getenv('OPENAI_API_KEY'))
        self.tts_engine = ChatterboxTTS()
        self.voice_trainer = VoiceTrainer()
    
    def convert(self, pdf_path, voice_model="default", summarize=False, output_format="mp3"):
        """Convert PDF to audiobook"""
        
        # Extract text from PDF
        text = self.pdf_extractor.extract_text(pdf_path)
        
        # Summarize if requested
        if summarize:
            text = self.summarizer.summarize_text(text, "book")
        
        # Generate unique output filename
        output_id = str(uuid.uuid4())
        output_path = f"outputs/audiobook_{output_id}.{output_format}"
        
        # Convert to speech
        audio_path = self.tts_engine.synthesize(text, voice_model, output_path)
        
        return {
            'output_path': audio_path,
            'text_length': len(text),
            'original_text': text[:500] + "..." if len(text) > 500 else text
        }

@celery.task
def convert_pdf_task(pdf_path, voice_model, summarize, output_format):
    """Background task for PDF conversion"""
    converter = PDFAudiobookConverter()
    return converter.convert(pdf_path, voice_model, summarize, output_format)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join('temp', filename)
        file.save(filepath)
        
        # Get conversion parameters
        voice_model = request.form.get('voice_model', 'default')
        summarize = request.form.get('summarize') == 'true'
        output_format = request.form.get('format', 'mp3')
        
        # Start background task
        task = convert_pdf_task.delay(filepath, voice_model, summarize, output_format)
        
        return jsonify({
            'task_id': task.id,
            'status': 'processing',
            'message': 'PDF conversion started'
        })
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/status/<task_id>')
def task_status(task_id):
    task = convert_pdf_task.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is waiting to be processed'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }
    
    return jsonify(response)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('temp', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=8000)
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## 📊 Performance Optimization

- **GPU Acceleration**: CUDA support for voice training and TTS
- **Batch Processing**: Efficient handling of large documents
- **Caching**: Redis-based caching for repeated conversions
- **Async Processing**: Celery for background tasks

## 🔒 Security Considerations

- File upload validation and sanitization
- Rate limiting for API endpoints
- Secure handling of API keys
- Input text sanitization for TTS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) for the TTS engine
- OpenAI for GPT integration
- The open-source community for various libraries and tools

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Join our Discord community: [link]

---

**Happy Audiobook Creating! 🎧📚**