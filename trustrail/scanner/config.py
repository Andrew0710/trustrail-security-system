class ScannerConfig:
    def __init__(self):
        # Enable/disable detectors
        self.enabled_detectors = {
            'aws': True,
            'gcp': True,
            'azure': True,
            'openai': True,
            'anthropic': True,
            'huggingface': True,
            'langchain': True,
            'github': True,
            'ssh': True,
            'docker': True,
            'stripe': True,
            'db': True,
        }
        # Entropy threshold
        self.entropy_threshold = 4.0

    def is_detector_enabled(self, detector_type):
        return self.enabled_detectors.get(detector_type, True)

config = ScannerConfig()