from .base_detector import BaseDetector

class GCPDetector(BaseDetector):
    def __init__(self):
        patterns = [
            r'"private_key_id"\s*:\s*"[^"]{40}"',  # Private key ID in JSON
            r'AIza[0-9A-Za-z-_]{35}',  # GCP API key pattern
        ]
        super().__init__('gcp_secret', patterns, entropy_check=False)  # JSON keys may not be high entropy