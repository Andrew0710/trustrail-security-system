from ..utils.entropy_utils import is_high_entropy

class BaseDetector:
    def __init__(self, secret_type, patterns, entropy_check=False):
        self.secret_type = secret_type
        self.patterns = patterns  # list of regex patterns
        self.entropy_check = entropy_check

    def detect(self, content):
        import re
        findings = []
        for pattern in self.patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if self.entropy_check and not is_high_entropy(match):
                    continue
                findings.append({
                    'type': self.secret_type,
                    'value': match,
                    'line': None  # Can add line number later
                })
        return findings