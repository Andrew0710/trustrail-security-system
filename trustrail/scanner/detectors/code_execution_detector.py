from .base_detector import BaseDetector

class CodeExecutionDetector(BaseDetector):
    def __init__(self):
        patterns = [r'\b(eval|exec)\s*\(']
        super().__init__('code_execution', patterns, entropy_check=False)
