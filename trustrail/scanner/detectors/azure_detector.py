from .base_detector import BaseDetector

class AzureDetector(BaseDetector):
    def __init__(self):
        patterns = [
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',  # Azure client ID/GUID
            r'[A-Za-z0-9+/=]{40,}',  # Azure access tokens (base64-like)
        ]
        super().__init__('azure_secret', patterns, entropy_check=True)