# Authentication module
import os

def get_api_key():
    # Anthropic API key
    return "sk-ant-1234567890abcdef1234567890abcdef1234567890abcdef"

def authenticate(user, password):
    # Dummy auth
    return user == "admin" and password == "password"
