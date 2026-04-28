# TrustRail

A high-performance Shift-Left Security ecosystem to prevent sensitive data leaks.

## Installation

Clone the repo and install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Scan a file or directory:

```bash
python -m cli.main scan /path/to/code
```

Fix secrets automatically:

```bash
python -m cli.main fix /path/to/file
```

### Git Hooks

TrustRail provides Git hooks to prevent secrets from entering your repository:

### Install Hooks

Run the following command inside your git repository:

```bash
cd /path/to/your/repo
python3 -m trustrail.cli.main install-hooks
```

This will install:
- **pre-commit**: Scans staged files before each commit. Blocks commit if secrets found.
- **pre-push**: Scans the entire project before push. Blocks push if secrets found.

### What Happens on Failure

If secrets are detected:
- **Commit blocked**: The commit is rejected. Fix the secrets or use `python3 -m cli.main fix <file>` to auto-remediate.
- **Push rejected**: The push is rejected. Review detected secrets, fix them, then try again.

### Uninstall Hooks

To remove hooks, delete the files:
```bash
rm .git/hooks/pre-commit .git/hooks/pre-push
```

## Frontend

To run the React dashboard:

```bash
cd frontend
npm run dev
```

The dashboard will be available at http://localhost:5173 (default Vite port).

## Backend

To run the telemetry backend:

```bash
cd backend/django_project
python manage.py migrate
python manage.py runserver
```

The API will be available at http://localhost:8000/api/incidents/ for the dashboard.