from .detectors.aws_detector import AWSDetector
from .detectors.gcp_detector import GCPDetector
from .detectors.azure_detector import AzureDetector
from .detectors.openai_detector import OpenAIDetector
from .detectors.anthropic_detector import AnthropicDetector
from .detectors.huggingface_detector import HuggingFaceDetector
from .detectors.langchain_detector import LangChainDetector
from .detectors.github_detector import GitHubDetector
from .detectors.ssh_detector import SSHDetector
from .detectors.docker_detector import DockerDetector
from .detectors.stripe_detector import StripeDetector
from .detectors.db_detector import DBDetector
from .detectors.slack_webhook_detector import SlackWebhookDetector
from .detectors.yaml_db_password_detector import YamlDBPasswordDetector
from .detectors.os_system_detector import OSSystemDetector
from .detectors.code_execution_detector import CodeExecutionDetector

class ScannerEngine:
    def __init__(self):
        self.detectors = [
            AWSDetector(),
            GCPDetector(),
            AzureDetector(),
            OpenAIDetector(),
            AnthropicDetector(),
            HuggingFaceDetector(),
            LangChainDetector(),
            GitHubDetector(),
            SSHDetector(),
            DockerDetector(),
            StripeDetector(),
            DBDetector(),
            SlackWebhookDetector(),
            YamlDBPasswordDetector(),
            OSSystemDetector(),
            CodeExecutionDetector(),
        ]
        # Description mapping for each secret type
        self.descriptions = {
            'aws_access_key': 'AWS Access Key ID found. Rotate the key immediately and remove it from the code.',
            'gcp_secret': 'GCP secret found. Rotate the key and remove it from the code.',
            'azure_secret': 'Azure secret found. Rotate the key and remove it from the code.',
            'openai_api_key': 'OpenAI API key found. Rotate the key and remove it from the code.',
            'anthropic_api_key': 'Anthropic API key found. Rotate the key and remove it from the code.',
            'huggingface_token': 'HuggingFace token found. Rotate the token and remove it from the code.',
            'github_pat': 'GitHub Personal Access Token found. Rotate the token and remove it from the code.',
            'ssh_private_key': 'SSH private key found. Replace with a new key pair and remove the private key from the code.',
            'docker_config': 'Docker configuration found. Remove sensitive auth data from the code.',
            'stripe_secret_key': 'Stripe secret key found. Rotate the key and remove it from the code.',
            'db_connection_string': 'Database connection string found. Use environment variables or a secrets manager and remove from the code.',
            'slack_webhook': 'Slack Webhook URL found. Rotate the webhook in Slack workspace settings.',
            'yaml_db_password': 'Database password found in YAML configuration. Move to environment variable or secrets manager.',
            'os_system': 'Security Vulnerability: os.system() call found. This can lead to command injection if used with unsanitized input.',
            'code_execution': 'Security Vulnerability: Dynamic code execution (eval/exec) found. Avoid using eval()/exec(); use safer alternatives.',
        }

    def get_description(self, secret_type):
        return self.descriptions.get(secret_type, 'Secret found. Remove it from the code and use a secure alternative.')

    def scan_file(self, file_path):
        """Scan a file for secrets. Returns list of findings."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [{'error': str(e), 'file': file_path}]

        findings = []
        lines = content.splitlines()
        for detector in self.detectors:
            results = detector.detect(content)
            for result in results:
                # Find the line containing the secret
                line_number = None
                line_content = None
                for i, line in enumerate(lines):
                    if result['value'] in line:
                        line_number = i + 1
                        line_content = line.rstrip('\n')
                        break
                finding = {
                    'type': result['type'],
                    'value': result['value'],
                    'file': file_path,
                    'line_number': line_number,
                    'line_content': line_content,
                    'description': self.get_description(result['type'])
                }
                findings.append(finding)
        return findings
