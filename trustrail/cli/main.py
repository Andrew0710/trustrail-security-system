import argparse
import sys
import os
import requests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scanner.engine import ScannerEngine
from remediation.quick_fix import QuickFix

# Backend API endpoint
API_URL = os.getenv('TRUSTRAIL_API_URL', 'http://127.0.0.1:8000/api/incidents/')

def send_incident_to_backend(secret_type, file_name, code_snippet, secret_value, description, project_name):
    """Send a detected incident to the backend API."""
    try:
        import hashlib
        user_id = os.getenv('TRUSTRAIL_USER_ID', 'cli_user')
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()
        payload = {
            'user_hash': user_hash,
            'secret_type': secret_type,
            'file_name': file_name,
            'code_snippet': code_snippet,
            'secret_value': secret_value,
            'description': description,
            'project_name': project_name
        }
        response = requests.post(API_URL, json=payload, timeout=5)
        return response.status_code == 201
    except Exception as e:
        print(f"  [WARN] Could not send incident to backend: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='TrustRail Secret Scanner')
    parser.add_argument('command', choices=['scan', 'fix', 'install-hooks'], help='Command to run')
    parser.add_argument('path', help='File or directory to scan', nargs='?', default=None)
    parser.add_argument('--project-name', default='CLI Scan', help='Name of the project for tagging incidents')

    args = parser.parse_args()

    if args.command == 'install-hooks':
        # Import here to avoid circular dependency if not installed
        try:
            from git_integration.install_hook import install_hooks
            install_hooks()
        except ImportError as e:
            print(f"Error importing hook installer: {e}")
            print("Make sure you are running from the trustrail package.")
        return

    # Existing scan/fix logic requires a path
    if args.path is None:
        parser.error("the following arguments are required: path")

    engine = ScannerEngine()
    fixer = QuickFix()

    total_findings = 0  # Track total secrets found

    def process_findings(findings, project_name):
        nonlocal total_findings
        sent_count = 0
        for finding in findings:
            if 'error' in finding:
                print(f"Error scanning {finding['file']}: {finding['error']}")
            else:
                total_findings += 1
                print(f"Found {finding['type']} in {finding['file']}: {finding['value']}")
                abs_path = os.path.abspath(finding['file'])
                if send_incident_to_backend(
                    secret_type=finding['type'],
                    file_name=abs_path,
                    code_snippet=finding.get('line_content'),
                    secret_value=finding.get('value'),
                    description=finding.get('description', 'Secret found in code'),
                    project_name=project_name
                ):
                    sent_count += 1
                if args.command == 'fix':
                    if fixer.apply_fix(finding):
                        print(f"  Fixed: Moved to .env and updated file.")
                    else:
                        print("  Could not auto-fix.")
        return sent_count

    if os.path.isfile(args.path):
        findings = engine.scan_file(args.path)
        sent = process_findings(findings, args.project_name)
        print(f"\n[sent {sent} incident(s) to dashboard]")
    else:
        total_sent = 0
        for root, dirs, files in os.walk(args.path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env', '.venv']]
            for file in files:
                if file.startswith('.'):
                    continue
                if file.endswith(('.py', '.js', '.ts', '.json', '.env', '.txt', '.yaml', '.yml')):
                    file_path = os.path.join(root, file)
                    findings = engine.scan_file(file_path)
                    sent = process_findings(findings, args.project_name)
                    total_sent += sent
        print(f"\n[Total: sent {total_sent} incident(s) to dashboard]")

    # Exit with code 1 if any secrets were found (to fail CI/hooks)
    if total_findings > 0:
        print(f"\n❌ Found {total_findings} secret(s). Exiting with failure.")
        sys.exit(1)
    else:
        print("\n✅ No secrets found.")
        sys.exit(0)

if __name__ == '__main__':
    main()
