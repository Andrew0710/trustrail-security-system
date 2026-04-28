# Test Project V2

A sample project for testing TrustRail secret scanner.

## Structure
```
test_project_v2/
├── config/
│   └── settings.py      # Django settings with secrets
├── scripts/
│   └── deploy.sh        # Deployment script with AWS keys
├── .env.example         # Environment file with fake secrets
├── src/
│   └── utils.py         # Clean utility functions (no secrets)
└── README.md
```

## Secrets intentionally placed:
- `config/settings.py`: Django SECRET_KEY, database password, GitHub PAT
- `scripts/deploy.sh`: AWS credentials
- `.env.example`: Stripe API key, OpenAI API key, database URL

## Usage
Run TrustRail scanner on this folder to detect all secrets:
```bash
python3 -m cli.main scan test_project_v2/
```