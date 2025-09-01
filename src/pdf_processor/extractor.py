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
