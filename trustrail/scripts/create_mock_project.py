#!/usr/bin/env python3
"""
Script to create a mock project with various files containing secrets for demo purposes.
Generates trustrail/tests/mock_project/ with files that have secrets and some clean ones.
"""

import os
import shutil

def create_mock_project():
    base_dir = "trustrail/tests/mock_project"
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    # Create config.py with AWS key
    with open(os.path.join(base_dir, "config.py"), "w") as f:
        f.write("""# Configuration file
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DEBUG = True
""")

    # Create api.py with OpenAI key
    with open(os.path.join(base_dir, "api.py"), "w") as f:
        f.write("""import openai

openai.api_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
client = openai.OpenAI()

def generate_response(prompt):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
""")

    # Create .env with various secrets
    with open(os.path.join(base_dir, ".env"), "w") as f:
        f.write("""# Environment variables
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
STRIPE_SECRET_KEY=sk_test_1234567890abcdef1234567890abcdef
GITHUB_TOKEN=ghp_1234567890abcdef1234567890abcdef12345678
""")

    # Create deploy.sh with SSH private key
    with open(os.path.join(base_dir, "deploy.sh"), "w") as f:
        f.write("""#!/bin/bash
# Deployment script

# SSH Private Key (should not be here!)
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDeFaqJLJY1yJ4qVO3FgqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q
5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5q
Kj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj
8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8qBqO6q5qKj8q
-----END OPENSSH PRIVATE KEY-----

scp -i ~/.ssh/id_rsa app.py user@server:/var/www/
""")

    # Create Dockerfile with auth
    with open(os.path.join(base_dir, "Dockerfile"), "w") as f:
        f.write("""FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
# Docker auth config (should not be here!)
{"auths":{"registry.example.com":{"auth":"dXNlcjpwYXNzd29yZA=="}}}""")

    # Create clean files
    with open(os.path.join(base_dir, "utils.py"), "w") as f:
        f.write("""# Utility functions
def calculate_total(items):
    return sum(item['price'] * item['quantity'] for item in items)

def format_date(date):
    return date.strftime('%Y-%m-%d')
""")

    # Create README.md (clean)
    with open(os.path.join(base_dir, "README.md"), "w") as f:
        f.write("""# Mock Project

This is a sample project for testing TrustRail scanner.

## Features
- Configuration management
- API integration
- Deployment scripts

## Usage
Run `python app.py` to start the application.
""")

    # Create subdir with more files
    sub_dir = os.path.join(base_dir, "src")
    os.makedirs(sub_dir)

    with open(os.path.join(sub_dir, "auth.py"), "w") as f:
        f.write("""# Authentication module
import os

def get_api_key():
    # Anthropic API key
    return "sk-ant-1234567890abcdef1234567890abcdef1234567890abcdef"

def authenticate(user, password):
    # Dummy auth
    return user == "admin" and password == "password"
""")

    with open(os.path.join(sub_dir, "database.py"), "w") as f:
        f.write("""# Database connection
import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="secretpassword123"
    )
    return conn
""")

    print(f"Mock project created at {base_dir}")
    print("Files with secrets:")
    print("- config.py (AWS keys)")
    print("- api.py (OpenAI key)")
    print("- .env (various secrets)")
    print("- deploy.sh (SSH private key)")
    print("- Dockerfile (Docker auth)")
    print("- src/auth.py (Anthropic key)")
    print("- src/database.py (DB password)")
    print("Clean files:")
    print("- utils.py")
    print("- README.md")

if __name__ == "__main__":
    create_mock_project()