from src.summarization.summarizer import LLMSummarizer

def test_llm_summarizer_instantiation():
    """
    Tests that the LLMSummarizer class can be instantiated.
    """
    try:
        _ = LLMSummarizer(api_key="test_key")
        assert True
    except Exception as e:
        assert False, f"Failed to instantiate LLMSummarizer: {e}"
