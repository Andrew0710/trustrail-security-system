from .base_detector import BaseDetector

class DBDetector(BaseDetector):
    def __init__(self):
        patterns = [
            r'postgresql://[^:]+:[^@]+@[^/]+/[^"]+',  # PostgreSQL
            r'mysql://[^:]+:[^@]+@[^/]+/[^"]+',      # MySQL
            r'redis://[^@]*:[^@]+@[^/]+',            # Redis
        ]
        super().__init__('db_connection_string', patterns, entropy_check=False)  # Connection strings may not be high entropy