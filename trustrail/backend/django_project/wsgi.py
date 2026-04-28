import os
from django.core.wsgi import get_wsgi_application

# Вказуємо на твій settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()