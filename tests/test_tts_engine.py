from src.tts_engine.chatterbox_wrapper import ChatterboxTTS

def test_chatterbox_tts_instantiation():
    """
    Tests that the ChatterboxTTS class can be instantiated.
    """
    try:
        _ = ChatterboxTTS()
        assert True
    except Exception as e:
        assert False, f"Failed to instantiate ChatterboxTTS: {e}"
