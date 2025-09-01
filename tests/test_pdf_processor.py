from src.pdf_processor.extractor import PDFExtractor

def test_pdf_extractor_instantiation():
    """
    Tests that the PDFExtractor class can be instantiated.
    """
    try:
        _ = PDFExtractor()
        assert True
    except Exception as e:
        assert False, f"Failed to instantiate PDFExtractor: {e}"
