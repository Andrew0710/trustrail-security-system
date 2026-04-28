from .base_detector import BaseDetector

class AnthropicDetector(BaseDetector):
    def __init__(self):
        patterns = [r'sk-ant-[a-zA-Z0-9_-]{95}']  # Anthropic API key
        super().__init__('anthropic_api_key', patterns, entropy_check=True)