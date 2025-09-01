from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from celery import Celery
import uuid

from src.pdf_processor.extractor import PDFExtractor
from src.summarization.summarizer import LLMSummarizer
from src.tts_engine.chatterbox_wrapper import ChatterboxTTS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Celery configuration
celery = Celery(app.name, broker='redis://localhost:6379')

class PDFAudiobookConverter:
    def __init__(self):
        self.pdf_extractor = PDFExtractor()
        self.summarizer = LLMSummarizer(api_key=os.getenv('OPENAI_API_KEY'))
        self.tts_engine = ChatterboxTTS()

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
