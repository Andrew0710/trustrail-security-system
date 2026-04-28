from .base_detector import BaseDetector

class DockerDetector(BaseDetector):
    def __init__(self):
        patterns = [
            r'"auth"\s*:\s*"[^"]{20,}"',  # Docker auth token in JSON
        ]
        super().__init__('docker_config', patterns, entropy_check=False)