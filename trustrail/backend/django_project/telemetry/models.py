from django.db import models
import hashlib

class Incident(models.Model):
    user_hash = models.CharField(max_length=64)  # hash of user identifier
    secret_type = models.CharField(max_length=100)
    file_name = models.CharField(max_length=255)
    code_snippet = models.TextField(blank=True, null=True)  # The actual line of code where secret was found
    secret_value = models.CharField(max_length=512, blank=True, null=True)  # The raw secret value
    description = models.TextField(blank=True, null=True)  # Description/recommendation for fixing
    project_name = models.CharField(max_length=255, blank=True, null=True)  # Name of the project being scanned
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure user_hash is hashed
        if not self.user_hash.startswith('hashed_'):
            self.user_hash = 'hashed_' + hashlib.sha256(self.user_hash.encode()).hexdigest()
        super().save(*args, **kwargs)
