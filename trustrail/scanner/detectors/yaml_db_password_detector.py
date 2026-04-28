from .base_detector import BaseDetector

class YamlDBPasswordDetector(BaseDetector):
    def __init__(self):
        # Detect password: "value" or 'value' in YAML config, at least 8 chars
        patterns = [
            r'(?i)password\s*:\s*"[^"]{8,}"',
            r"(?i)password\s*:\s*'[^']{8,}'"
        ]
        super().__init__('yaml_db_password', patterns, entropy_check=False)
