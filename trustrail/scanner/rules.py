"""
Centralized Security Rules Library for TrustRail SAST Engine.

Each rule is a dictionary with:
- type: unique identifier
- category: "Secret" or "Vulnerability"
- severity: "Critical", "High", "Medium", "Low"
- pattern: regex pattern to match
- recommendation: specific remediation advice
"""

# Secret Detection Rules (Existing)
SECRET_RULES = {
    'aws_access_key': {
        'type': 'aws_access_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'AKIA[0-9A-Z]{16}',
        'recommendation': 'AWS Access Key ID found. Rotate the key immediately using AWS IAM console and remove from code.'
    },
    'aws_secret_key': {
        'type': 'aws_secret_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'[A-Za-z0-9+/]{40}',  # Simplified; real secret keys are longer base64
        'recommendation': 'AWS Secret Access Key found. Rotate immediately using AWS IAM console.'
    },
    'github_pat': {
        'type': 'github_pat',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'ghp_[0-9a-zA-Z]{36}',
        'recommendation': 'GitHub Personal Access Token found. Revoke the token and create a new one.'
    },
    'openai_api_key': {
        'type': 'openai_api_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'sk-[a-zA-Z0-9]{32,}',
        'recommendation': 'OpenAI API key found. Revoke the key in OpenAI dashboard and create a new one.'
    },
    'slack_webhook': {
        'type': 'slack_webhook',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}',
        'recommendation': 'Slack Webhook URL found. Rotate the webhook in Slack workspace settings.'
    },
    'yaml_db_password': {
        'type': 'yaml_db_password',
        'category': 'Secret',
        'severity': 'High',
        'pattern': "(?i)password\\s*:\\s*([\"'])([^\"']{8,})\\1",
        'recommendation': 'Database password found in YAML configuration. Move to environment variable or secrets manager.'
    },
    'slack_webhook': {
        'type': 'slack_webhook',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}',
        'recommendation': 'Slack Webhook URL found. Rotate the webhook in Slack workspace settings.'
    },
    'yaml_db_password': {
        'type': 'yaml_db_password',
        'category': 'Secret',
        'severity': 'High',
        'pattern': r'(?i)password\s*:\s*["\'][^"\']{8,}["\']',
        'recommendation': 'Database password found in YAML configuration. Move to environment variable or secrets manager.'
    },
    'stripe_secret_key': {
        'type': 'stripe_secret_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'sk_live_[0-9a-zA-Z]{24}',
        'recommendation': 'Stripe secret key found. Rotate the key immediately in Stripe dashboard.'
    },
    'db_connection_string': {
        'type': 'db_connection_string',
        'category': 'Secret',
        'severity': 'High',
        'pattern': r'(postgresql|mysql|redis)://[^:]+:[^@]+@[^/]+',
        'recommendation': 'Database connection string with credentials found. Use environment variables or a secrets manager.'
    },
    'ssh_private_key': {
        'type': 'ssh_private_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
        'recommendation': 'SSH private key found. Generate a new key pair and remove the private key from code.'
    },
    'gcp_secret': {
        'type': 'gcp_secret',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'AIza[0-9A-Za-z-_]{35}',
        'recommendation': 'GCP API key found. Revoke and rotate in Google Cloud Console.'
    },
    'azure_secret': {
        'type': 'azure_secret',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
        'recommendation': 'Azure secret found. Rotate the key in Azure Active Directory.'
    },
    'anthropic_api_key': {
        'type': 'anthropic_api_key',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'sk-ant-[a-zA-Z0-9_-]{95}',
        'recommendation': 'Anthropic API key found. Revoke and generate a new key in Anthropic console.'
    },
    'huggingface_token': {
        'type': 'huggingface_token',
        'category': 'Secret',
        'severity': 'Critical',
        'pattern': r'hf_[a-zA-Z0-9]{34}',
        'recommendation': 'HuggingFace token found. Revoke the token in HuggingFace settings.'
    },
    'docker_config': {
        'type': 'docker_config',
        'category': 'Secret',
        'severity': 'High',
        'pattern': r'"auth"\s*:\s*"[^"]{20,}"',
        'recommendation': 'Docker authentication data found. Remove from code and use docker login or environment variables.'
    },
}

# Vulnerability Detection Rules (New)
VULNERABILITY_RULES = {
    'os_injection': {
        'type': 'os_injection',
        'category': 'Vulnerability',
        'severity': 'Critical',
        'pattern': r'(os\.system|os\.popen|subprocess\.Popen)\s*\(\s*[^)]*shell\s*=\s*True',
        'recommendation': 'OS command injection risk. Use subprocess.run(shell=False) with a list of arguments instead.',
        'language': 'python'
    },
    'code_execution': {
        'type': 'code_execution',
        'category': 'Vulnerability',
        'severity': 'Critical',
        'pattern': r'\b(eval|exec)\s*\(',
        'recommendation': 'Dynamic code execution found. Avoid eval()/exec(); use safer alternatives like ast.literal_eval() or function maps.'
    },
    'os_system': {
        'type': 'os_system',
        'category': 'Vulnerability',
        'severity': 'Critical',
        'pattern': r'\bos\.system\s*\(',
        'recommendation': 'Avoid os.system() as it can lead to command injection. Use subprocess.run(shell=False) with a list of arguments.'
    },
    'os_system': {
        'type': 'os_system',
        'category': 'Vulnerability',
        'severity': 'Critical',
        'pattern': r'\bos\.system\s*\(',
        'recommendation': 'Avoid os.system() as it can lead to command injection. Use subprocess.run(shell=False) with a list of arguments.'
    },
    'sql_injection': {
        'type': 'sql_injection',
        'category': 'Vulnerability',
        'severity': 'Critical',
        'pattern': r'(execute|executemany)\s*\(\s*f["\'].*SELECT.*WHERE',
        'recommendation': 'Potential SQL injection via string formatting. Use parameterized queries with placeholders (e.g., ? or %s).',
        'language': 'python'
    },
    'insecure_crypto_md5': {
        'type': 'insecure_crypto_md5',
        'category': 'Vulnerability',
        'severity': 'Medium',
        'pattern': r'hashlib\.md5\s*\(',
        'recommendation': 'MD5 is cryptographically broken. Use SHA-256 or SHA-3 for cryptographic purposes.',
        'language': 'python'
    },
    'insecure_crypto_sha1': {
        'type': 'insecure_crypto_sha1',
        'category': 'Vulnerability',
        'severity': 'Medium',
        'pattern': r'hashlib\.sha1\s*\(',
        'recommendation': 'SHA-1 is deprecated for security. Use SHA-256 or SHA-3 instead.',
        'language': 'python'
    },
    'hardcoded_password': {
        'type': 'hardcoded_password',
        'category': 'Vulnerability',
        'severity': 'High',
        'pattern': r'(password|passwd|pwd)\s*=\s*["\'][^"\']{8,}["\']',
        'recommendation': 'Hardcoded password found. Store passwords in environment variables or use a secrets manager.',
        'language': 'python'
    },
    'debug_mode': {
        'type': 'debug_mode',
        'category': 'Vulnerability',
        'severity': 'Low',
        'pattern': r'DEBUG\s*=\s*True',
        'recommendation': 'Debug mode enabled in production. Set DEBUG=False in production to prevent information leakage.',
        'language': 'python'
    },
}

# Combine all rules
ALL_RULES = {**SECRET_RULES, **VULNERABILITY_RULES}

def get_rule(rule_type):
    """Return rule dictionary by type."""
    return ALL_RULES.get(rule_type)

def get_rules_by_category(category):
    """Return all rules of a given category."""
    return [rule for rule in ALL_RULES.values() if rule['category'] == category]

def get_available_rule_types():
    """Return list of all rule types."""
    return list(ALL_RULES.keys())