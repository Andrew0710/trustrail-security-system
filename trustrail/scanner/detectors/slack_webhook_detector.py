from .base_detector import BaseDetector

class SlackWebhookDetector(BaseDetector):
    def __init__(self):
        patterns = [r'https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}']
        super().__init__('slack_webhook', patterns, entropy_check=False)
