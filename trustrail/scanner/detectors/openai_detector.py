from .base_detector import BaseDetector

class OpenAIDetector(BaseDetector):
    def __init__(self):
        patterns = [r'sk-[a-zA-Z0-9]{32,}']  # OpenAI API key pattern
        super().__init__('openai_api_key', patterns, entropy_check=True)