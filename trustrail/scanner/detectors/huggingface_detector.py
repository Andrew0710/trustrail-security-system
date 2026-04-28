from .base_detector import BaseDetector

class HuggingFaceDetector(BaseDetector):
    def __init__(self):
        patterns = [r'hf_[a-zA-Z0-9]{34}']  # HuggingFace API token
        super().__init__('huggingface_token', patterns, entropy_check=True)