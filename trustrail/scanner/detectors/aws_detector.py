from .base_detector import BaseDetector

class AWSDetector(BaseDetector):
    def __init__(self):
        patterns = [r'AKIA[0-9A-Z]{16}']  # AWS Access Key ID
        super().__init__('aws_access_key', patterns, entropy_check=False)