from setuptools import setup, find_packages

setup(
    name="pdf_audiobook_ai",
    version="0.1.0",
    description="An intelligent AI voice agent that converts PDFs into high-quality audiobooks.",
    author="AI Agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=1.9.0",
        "torchaudio>=0.9.0",
        "transformers>=4.20.0",
        "openai>=0.27.0",
        "PyPDF2>=2.10.0",
        "pdfplumber>=0.7.0",
        "pytesseract>=0.3.10",
        "librosa>=0.9.0",
        "soundfile>=0.10.0",
        "flask>=2.0.0",
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "celery>=5.2.0",
        "redis>=4.0.0",
        "PyMuPDF",
        "tiktoken",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
