#!/usr/bin/env python3
"""
TrustRail Git Hooks Installer

Installs both pre-commit and pre-push hooks into the current git repository.
"""

import os
import shutil
import stat
import sys

def install_hooks():
    # Determine the project root (where this script resides)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # trustrail/
    hooks_source_dir = os.path.join(project_root, 'scripts')

    # Get the absolute path to the current Python interpreter (where trustrail is installed)
    python_executable = sys.executable

    # Check if we're in a git repo
    if not os.path.exists('.git'):
        print("❌ Not a git repository. Please run this inside a git repo.")
        return False

    hooks_dest_dir = os.path.join('.git', 'hooks')
    if not os.path.exists(hooks_dest_dir):
        print("❌ .git/hooks directory not found.")
        return False

    def install_hook(source_name, dest_name):
        source_path = os.path.join(hooks_source_dir, source_name)
        dest_path = os.path.join(hooks_dest_dir, dest_name)
        if os.path.exists(source_path):
            with open(source_path, 'r') as f:
                content = f.read()
            # Replace placeholders with actual paths
            content = content.replace('__TRUSTRAIL_PATH__', project_root)
            content = content.replace('__PYTHON__', python_executable)
            with open(dest_path, 'w') as f:
                f.write(content)
            os.chmod(dest_path, os.stat(dest_path).st_mode | stat.S_IEXEC)
            print(f"✅ Installed {dest_name} hook")
            return True
        else:
            print(f"⚠️  {source_name} not found at {source_path}")
            print(f"   (looked for: {source_path})")
            return False

    # Install both hooks
    install_hook('git-pre-commit.sh', 'pre-commit')
    install_hook('git-pre-push.sh', 'pre-push')

    print("\n🎉 TrustRail hooks installed!")
    print("   - pre-commit: Scans project before commit")
    print("   - pre-push: Scans project before push")
    print("\nTrustRail will now protect your repository.")
    return True

if __name__ == '__main__':
    install_hooks()