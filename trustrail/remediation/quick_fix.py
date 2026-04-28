import os
import re

class QuickFix:
    def __init__(self):
        self.env_file = '.env'

    def apply_fix(self, finding):
        file_path = finding['file']
        secret = finding['value']
        secret_type = finding['type']

        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except Exception:
            return False

        # Find the line with the secret, assume var = "secret"
        pattern = rf'(\w+)\s*=\s*["\']({re.escape(secret)})["\']'
        match = re.search(pattern, content)
        if not match:
            return False

        var_name = match.group(1).upper()

        # Replace in file
        new_content = re.sub(pattern, f'{match.group(1)} = os.getenv(\'{var_name}\')', content)
        with open(file_path, 'w') as f:
            f.write(new_content)

        # Add to .env
        env_line = f'{var_name}={secret}\n'
        if os.path.exists(self.env_file):
            with open(self.env_file, 'a') as f:
                f.write(env_line)
        else:
            with open(self.env_file, 'w') as f:
                f.write(env_line)

        # Update .gitignore
        self.update_gitignore()

        return True

    def update_gitignore(self):
        gitignore = '.gitignore'
        if os.path.exists(gitignore):
            with open(gitignore, 'r') as f:
                content = f.read()
            if '.env' not in content:
                with open(gitignore, 'a') as f:
                    f.write('\n.env\n')
        else:
            with open(gitignore, 'w') as f:
                f.write('.env\n')