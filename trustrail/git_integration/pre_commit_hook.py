#!/usr/bin/env python3
import sys
import os
import subprocess

# Add trustrail to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.engine import ScannerEngine
from remediation.quick_fix import QuickFix

def get_staged_files():
    """Get list of staged files."""
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception:
        return []

def main():
    engine = ScannerEngine()
    fixer = QuickFix()
    staged_files = get_staged_files()
    all_findings = []

    # Scan staged files
    for file in staged_files:
        if os.path.exists(file) and file.endswith(('.py', '.js', '.ts', '.json', '.env', '.txt')):  # Scan relevant files
            findings = engine.scan_file(file)
            if findings:
                all_findings.extend(findings)

    if all_findings:
        print("🚫 Secrets detected in staged files. Attempting automatic remediation...")
        fixed = False
        for finding in all_findings:
            if 'error' not in finding and fixer.apply_fix(finding):
                print(f"  Fixed {finding['type']} in {finding['file']}")
                fixed = True

        if fixed:
            # Rescan after fixes
            all_findings = []
            for file in staged_files:
                if os.path.exists(file) and file.endswith(('.py', '.js', '.ts', '.json', '.env', '.txt')):
                    findings = engine.scan_file(file)
                    if findings:
                        all_findings.extend(findings)

        if all_findings:
            print("❌ Some secrets could not be fixed automatically. Commit blocked:")
            for finding in all_findings:
                if 'error' not in finding:
                    print(f"  {finding['type']} in {finding['file']}: {finding['value']}")
            print("Please manually remove secrets or run 'python -m cli.main fix <file>' to fix.")
            sys.exit(1)
        else:
            print("✅ Secrets fixed automatically. Proceeding with commit.")
    else:
        print("✅ No secrets detected. Proceeding with commit.")

if __name__ == '__main__':
    main()