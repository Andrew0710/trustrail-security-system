from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'user_hash', 'secret_type', 'file_name', 'code_snippet', 'secret_value', 'description', 'project_name', 'timestamp']
