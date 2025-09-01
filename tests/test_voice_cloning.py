from src.voice_cloning.trainer import VoiceTrainer

def test_voice_trainer_instantiation():
    """
    Tests that the VoiceTrainer class can be instantiated.
    """
    # The VoiceTrainer expects a config object with attribute access.
    class MockConfig:
        def __init__(self, batch_size):
            self.batch_size = batch_size

    try:
        config = MockConfig(batch_size=32)
        _ = VoiceTrainer(config=config)
        assert True
    except Exception as e:
        assert False, f"Failed to instantiate VoiceTrainer: {e}"
