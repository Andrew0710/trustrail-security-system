from .base_detector import BaseDetector

class OSSystemDetector(BaseDetector):
    def __init__(self):
        patterns = [r'\bos\.system\s*\(']
        super().__init__('os_system', patterns, entropy_check=False)
