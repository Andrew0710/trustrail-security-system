# TrustRail

> **Zero-leak policy. Automated Telemetry. Pre-commit Shield.**

**TrustRail** is a high-performance secret scanner and SAST tool that prevents sensitive data leaks before they reach your repository. Built for developer workflows, it combines regex-based secret detection with security vulnerability scanning, automated telemetry, and Git integration to enforce a shift-left security culture.

---

## Core Features

| Category | Capabilities |
|----------|--------------|
| **Secret Detection** | AWS, GCP, Azure, OpenAI, Anthropic, HuggingFace, GitHub PATs, SSH keys, Docker configs, Stripe, database passwords, Slack webhooks |
| **SAST Rules** | `os.system()`, `eval()`, `exec()`, hardcoded passwords, insecure crypto (MD5/SHA1), `DEBUG=True` |
| **Git Integration** | Pre-commit and pre-push hooks to block secrets at commit time |
| **Auto-Fix** | Moves hardcoded secrets to `.env` files and updates code to use `os.getenv()` |
| **Telemetry** | Django REST API backend to log incidents to a centralized dashboard |
| **File Support** | `.py`, `.js`, `.ts`, `.json`, `.env`, `.yaml`, `.yml`, `.txt` |
| **Privacy-First** | Local-first scanning; only anonymized metadata sent to backend |

---

## Architecture

```
┌─────────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│   Developer     │     │  TrustRail CLI      │     │  Django Backend  │
│   Workstation   │◄────┤  (Python Engine)    │◄────┤  (REST API)      │
│                 │     │                     │     │                  │
│  • Source code  │     │  • Scanner engine   │     │  • Incident      │
│  • Git repo     │     │  • Detectors        │     │    model         │
│                 │     │  • Remediation      │     │  • Serializers   │
└────────┬────────┘     └──────────┬──────────┘     └────────┬─────────┘
         │                        │                         │
         │      ┌─────────────────┴─────────────┐           │
         │      │   Detector Modules (Regex)    │           │
         │      │  • AWS / GCP / Azure          │           │
         │      │  • OpenAI / Anthropic         │           │
         │      │  • GitHub / SSH / Docker      │           │
         │      │  • Stripe / DB / Slack        │           │
         │      │  • Code execution / OS inject │           │
         │      └─────────────────┬─────────────┘           │
         │                        │                         │
         │      ┌─────────────────┴─────────────┐           │
         │      │   Remediation & Hooks          │           │
         │      │  • QuickFix (.env generation)  │           │
         │      │  • pre-commit hook             │           │
         │      │  • pre-push hook               │           │
         │      └────────────────────────────────┘           │
         │                                                    │
         └────────────────────┬───────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  Dashboard (React) │
                    │  • Incident trends │
                    │  • Severity stats  │
                    │  • User metrics    │
                    └────────────────────┘
```

**Key Components:**

- **CLI Engine** (`trustrail/cli/main.py`): Entry point for `scan`, `fix`, `install-hooks` commands
- **Scanner Engine** (`trustrail/scanner/engine.py`): Orchestrates all detectors
- **Detectors** (`trustrail/scanner/detectors/`): Modular regex-based detectors per secret/vulnerability type
- **Remediation** (`trustrail/remediation/quick_fix.py`): Auto-moves secrets to `.env` and updates code
- **Git Hooks** (`trustrail/git_integration/`): Pre-commit/pre-push blocking
- **Backend** (`trustrail/backend/django_project/`): Django + DRF API for telemetry ingestion
- **Dashboard**: React frontend (in `frontend/`) consuming REST API

---

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>/trustrail.git
cd trustrail

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install TrustRail in editable mode
pip install -e .

# 5. Set up the Django backend database
cd backend/django_project
python manage.py migrate
python manage.py collectstatic --noinput  # optional for production

# 6. (Optional) Create a superuser for dashboard admin access
python manage.py createsuperuser

# 7. Start the backend server (runs on http://127.0.0.1:8000)
python manage.py runserver
```

---

## Development Commands

### Hard Reset (Database)

If the Django backend database becomes corrupted or you need a clean slate:

```bash
cd backend/django_project

# 1. Remove the SQLite database
rm db.sqlite3

# 2. Delete all migration files (except __init__.py in each migrations folder)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 3. Recreate migrations from scratch
python manage.py makemigrations telemetry

# 4. Apply migrations
python manage.py migrate

# 5. Create a new admin user
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

### Common Development Tasks

```bash
# Run the scanner on a directory
trustrail scan /path/to/project

# Install Git hooks into the current repository
trustrail install-hooks

# Auto-fix detected secrets (interactive)
trustrail fix /path/to/file.py

# Run Django backend tests (if any)
python manage.py test

# Start React frontend (development)
cd frontend
npm install
npm run dev
```

---

## Usage

### Scanning a Project

```bash
# Scan a single file
trustrail scan app/config.py

# Scan an entire directory (recursively)
trustrail scan ./myproject --project-name "MyApp"

# Example output:
#
# 🔍 TrustRail: Scanning for secrets...
# Found aws_access_key in app/config.py: AKIAIOSFODNN7EXAMPLE
# Found github_pat in .github/workflows/deploy.yml: ghp_1234567890abcdefghijklmnopqrstuv
# Found openai_api_key in src/ai.py: sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ123456
# 
# [sent 3 incident(s) to dashboard]
# 
# ❌ Found 3 secret(s). Exiting with failure.
```

### Installing Git Hooks

```bash
# Navigate to your project root and install TrustRail hooks
cd /path/to/your/project
trustrail install-hooks

# Output:
# ✅ Installed pre-commit hook
# ✅ Installed pre-push hook
# 
# 🎉 TrustRail hooks installed!
#    - pre-commit: Scans project before commit
#    - pre-push: Scans project before push
# 
# TrustRail will now protect your repository.
```

Now every `git commit` and `git push` will automatically scan for secrets and block if any are found.

### Auto-Fixing Secrets

```bash
# Scan and fix in one step
trustrail fix app/config.py

# Output:
# Found aws_access_key in app/config.py: AKIAIOSFODNN7EXAMPLE
#   Fixed: Moved to .env and updated file.

# The file `app/config.py` is updated to:
#   AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#
# And `.env` now contains:
#   AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
```

---

## Configuration

TrustRail reads the following environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `TRUSTRAIL_API_URL` | Backend telemetry endpoint URL | `http://127.0.0.1:8000/api/incidents/` |
| `TRUSTRAIL_USER_ID` | Unique user identifier (hashed for anonymity) | `cli_user` |

**Example:**

```bash
export TRUSTRAIL_API_URL="https://telemetry.yourcompany.com/api/incidents/"
export TRUSTRAIL_USER_ID="user@example.com"
trustrail scan ./src
```

---

## Rule References

TrustRail's detection is based on the centralized rule library in `scanner/rules.py`:

### Secret Detection Patterns

| Type | Pattern | Example |
|------|---------|---------|
| `aws_access_key` | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| `aws_secret_key` | `[A-Za-z0-9+/]{40}` | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `github_pat` | `ghp_[0-9a-zA-Z]{36}` | `ghp_1234567890abcdefghijklmnopqrstuv` |
| `openai_api_key` | `sk-[a-zA-Z0-9]{32,}` | `sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ123456` |
| `anthropic_api_key` | `sk-ant-[a-zA-Z0-9_-]{95}` | `sk-ant-api03-...` |
| `huggingface_token` | `hf_[a-zA-Z0-9]{34}` | `hf_1234567890abcdefghijklmnopqrstuv` |
| `gcp_secret` | `AIza[0-9A-Za-z-_]{35}` | `AIzaSyD-EXAMPLEKEY` |
| `azure_secret` | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` | `12345678-1234-1234-1234-123456789abc` |
| `ssh_private_key` | `-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----` | `-----BEGIN RSA PRIVATE KEY-----` |
| `stripe_secret_key` | `sk_test_[0-9a-zA-Z]{24}` | `sk_test_1234567890abcdefghijklmn` |
| `slack_webhook` | `https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}` | `https://hooks.slack.com/services/...` |
| `docker_config` | `"auth"\s*:\s*"[^"]{20,}"` | `"auth": "eyJ1c2VyIjoi..."` |
| `db_connection_string` | `(postgresql|mysql|redis)://[^:]+:[^@]+@[^/]+` | `postgresql://user:pass@localhost/db` |
| `yaml_db_password` | `(?i)password\s*:\s*["\'][^"\']{8,}["\']` | `password: "s3cr3tP@ss"` |

### SAST Vulnerability Patterns

| Type | Pattern | Severity |
|------|---------|----------|
| `os_system` | `\bos\.system\s*\(` | Critical |
| `code_execution` | `\b(eval|exec)\s*\(` | Critical |
| `os_injection` | `(os\.system|os\.popen|subprocess\.Popen)\s*\(\s*[^)]*shell\s*=\s*True` | Critical |
| `sql_injection` | `(execute|executemany)\s*\(\s*f["\'].*SELECT.*WHERE` | Critical |
| `hardcoded_password` | `(password|passwd|pwd)\s*=\s*["\'][^"\']{8,}["\']` | High |
| `insecure_crypto_md5` | `hashlib\.md5\s*\(` | Medium |
| `insecure_crypto_sha1` | `hashlib\.sha1\s*\(` | Medium |
| `debug_mode` | `DEBUG\s*=\s*True` | Low |

---

## Dashboard

Once the Django backend is running, access the admin dashboard at:

```
http://127.0.0.1:8000/admin/
```

Login with the superuser credentials created via `createsuperuser`.

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/telemetry/` | POST | Log an incident (used by CLI) |
| `/api/incidents/` | GET | List all incidents (JSON) |
| `/api/incidents/` | POST | Create incident manually |
| `/api/incidents/` | DELETE | Delete all incidents |
| `/api/scan-snippet/` | POST | Scan code snippet & log results |
| `/api/remediate/` | POST | Trigger automatic remediation for an incident |

---

## Development

### Project Structure

```
trustrail/
├── cli/
│   └── main.py                 # CLI entry point (trustrail command)
├── scanner/
│   ├── engine.py               # ScannerEngine orchestrator
│   ├── rules.py                # Central rule definitions
│   ├── detectors/              # Modular detector classes
│   │   ├── aws_detector.py
│   │   ├── openai_detector.py
│   │   ├── os_system_detector.py
│   │   └── ... (14 detectors total)
│   └── utils/
│       └── entropy_utils.py    # Entropy analysis helpers
├── remediation/
│   └── quick_fix.py            # Auto-fix logic (secret → .env)
├── git_integration/
│   ├── install_hook.py         # Hook installer
│   └── pre_commit_hook.py      # Hook runner
├── telemetry/
│   └── client.py               # Anonymized telemetry sender
├── backend/
│   └── django_project/
│       ├── manage.py
│       ├── settings.py
│       ├── urls.py
│       └── telemetry/
│           ├── models.py       # Incident model
│           ├── views.py        # DRF views
│           ├── serializers.py
│           └── urls.py
├── frontend/                   # React dashboard (Vite + Tailwind)
├── scripts/
│   ├── git-pre-commit.sh       # Pre-commit hook script
│   └── git-pre-push.sh         # Pre-push hook script
├── tests/                      # Unit & integration tests
└── setup.py                    # Package installation config
```

### Adding a New Detector

1. **Create detector class** in `scanner/detectors/`:

```python
# scanner/detectors/mynew_detector.py
from .base_detector import BaseDetector

class MyNewDetector(BaseDetector):
    def detect(self, content):
        findings = []
        pattern = r'my-secret-pattern-here'
        for match in re.finditer(pattern, content):
            findings.append({
                'type': 'my_secret_type',
                'value': match.group(),
                'line': match.start()
            })
        return findings
```

2. **Register in `engine.py`**:

```python
from .detectors.mynew_detector import MyNewDetector

class ScannerEngine:
    def __init__(self):
        self.detectors = [
            # ... existing detectors ...
            MyNewDetector(),  # ← add here
        ]
```

3. **Add description in `engine.py`**:

```python
self.descriptions = {
    # ... existing ...
    'my_secret_type': 'My new secret found. Rotate immediately.',
}
```

4. **Define rule in `rules.py`** (optional, for centralized rule management):

```python
'my_secret_type': {
    'type': 'my_secret_type',
    'category': 'Secret',
    'severity': 'Critical',
    'pattern': r'my-secret-pattern-here',
    'recommendation': 'Rotate the secret immediately.'
}
```

5. **Update remediation mapping** in `backend/django_project/telemetry/views.py` (`RemediateView`) if auto-fix should be supported.

---

## Disclaimer

**TrustRail is a security tool, not a silver bullet.**

- Use TrustRail as part of a defense-in-depth strategy. It complements, but does not replace, code reviews, security audits, and dedicated secret management solutions (e.g., HashiCorp Vault, AWS Secrets Manager).
- Detection accuracy depends on regularly updated patterns. Maintain and extend detectors to match your organization's tech stack.
- The auto-fix feature modifies source files. Always review changes before committing.
- Telemetry data is anonymized, but comply with your organization's data privacy policies before enabling cloud reporting.
- The authors assume no liability for security incidents, data leaks, or damages arising from TrustRail usage. You are responsible for proper configuration, secret rotation, and secure handling of detected credentials.

**Security best practices:**
- Rotate all detected secrets immediately via the respective provider's console.
- Store production credentials in dedicated secrets managers, never in code.
- Audit telemetry access and restrict dashboard permissions.
- Keep TrustRail updated to benefit from the latest detection patterns.

---

## Maintainers

**Team GLAS** — [GitHub Organization]

TrustRail is maintained by Team GLAS, dedicated to building developer-first security tooling that doesn't get in the way.

---

## License

Distributed under the MIT License. See `LICENSE` file for details.

---

> **Built for developers. Secured by TrustRail.**