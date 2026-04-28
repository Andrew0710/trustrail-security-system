from .base_detector import BaseDetector

class GitHubDetector(BaseDetector):
    def __init__(self):
        patterns = [r'ghp_[a-zA-Z0-9]{36}']  # GitHub Personal Access Token
        super().__init__('github_pat', patterns, entropy_check=True)