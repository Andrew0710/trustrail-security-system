# Django settings with secrets (DO NOT COMMIT)

SECRET_KEY = 'django-insecure-fake-secret-key-change-this-in-production-1234567890'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'SuperSecretPassword123!',  # <-- Secret in code
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Another hardcoded secret
os.getenv(\'GITHUB_TOKEN\')