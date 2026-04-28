from .base_detector import BaseDetector

class SSHDetector(BaseDetector):
    def __init__(self):
        patterns = [
            r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',  # SSH private key headers
            r'-----BEGIN PRIVATE KEY-----',
        ]
        super().__init__('ssh_private_key', patterns, entropy_check=False)  # Keys are structured