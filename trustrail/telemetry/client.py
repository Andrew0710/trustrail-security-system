import requests
import hashlib
import os

class TelemetryClient:
    def __init__(self, backend_url='http://localhost:8000/api/telemetry/'):
        self.backend_url = backend_url

    def send_incident(self, user_id, secret_type, file_name):
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()
        data = {
            'user_hash': user_hash,
            'secret_type': secret_type,
            'file_name': file_name,
        }
        try:
            response = requests.post(self.backend_url, json=data)
            return response.status_code == 201
        except Exception:
            return False