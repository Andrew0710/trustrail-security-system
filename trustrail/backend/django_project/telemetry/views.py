from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Incident
from .serializers import IncidentSerializer
import tempfile
import os
import sys
import re

@method_decorator(csrf_exempt, name='dispatch')
class TelemetryView(APIView):
    def post(self, request):
        data = request.data
        user_hash = data.get('user_hash')
        secret_type = data.get('secret_type')
        file_name = data.get('file_name')

        if not all([user_hash, secret_type, file_name]):
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        incident = Incident.objects.create(
            user_hash=user_hash,
            secret_type=secret_type,
            file_name=file_name
        )
        return Response({'id': incident.id}, status=status.HTTP_201_CREATED)

class IncidentList(ListCreateAPIView):
    queryset = Incident.objects.all().order_by('-timestamp')
    serializer_class = IncidentSerializer

    def delete(self, request, *args, **kwargs):
        # Delete all incidents
        deleted_count, _ = Incident.objects.all().delete()
        return Response({'deleted': deleted_count}, status=status.HTTP_204_NO_CONTENT)

@method_decorator(csrf_exempt, name='dispatch')
class ScanSnippetView(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Add the project root to sys.path so we can import scanner.engine
            current_dir = os.path.dirname(os.path.abspath(__file__))
            trustrail_path = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            sys.path.insert(0, trustrail_path)

            from scanner.engine import ScannerEngine
            fd, temp_path = tempfile.mkstemp(suffix='.py')
            try:
                with os.fdopen(fd, 'w') as f:
                    f.write(code)
                engine = ScannerEngine()
                findings = engine.scan_file(temp_path)
                saved_incidents = []
                for finding in findings:
                    if 'error' not in finding:
                        incident = Incident.objects.create(
                            user_hash='demo_user',
                            secret_type=finding['type'],
                            file_name='scan_snippet.py',
                            code_snippet=finding.get('line_content'),
                            secret_value=finding.get('value'),
                            description=finding.get('description')
                        )
                        saved_incidents.append(incident.id)
                return Response({
                    'findings': findings,
                    'saved_incidents': saved_incidents
                }, status=status.HTTP_200_OK)
            finally:
                os.unlink(temp_path)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class RemediateView(APIView):
    def post(self, request):
        try:
            incident_id = request.data.get('incident_id')
            if not incident_id:
                return Response({'error': 'Incident ID required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                incident = Incident.objects.get(id=incident_id)
            except Incident.DoesNotExist:
                return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)

            file_path = incident.file_name
            secret_value = incident.secret_value  # raw secret value
            secret_type = incident.secret_type

            if not secret_value:
                return Response({'error': 'No secret value stored for this incident'}, status=status.HTTP_400_BAD_REQUEST)

            # Determine environment variable name from secret type
            env_var_map = {
                'aws_access_key': 'AWS_ACCESS_KEY_ID',
                'aws_secret_key': 'AWS_SECRET_ACCESS_KEY',
                'github_pat': 'GITHUB_TOKEN',
                'openai_api_key': 'OPENAI_API_KEY',
                'stripe_secret_key': 'STRIPE_SECRET_KEY',
                'gcp_secret': 'GCP_API_KEY',
                'azure_secret': 'AZURE_TOKEN',
                'huggingface_token': 'HUGGINGFACE_TOKEN',
                'anthropic_api_key': 'ANTHROPIC_API_KEY',
                'langchain_key': 'LANGCHAIN_KEY',
                'ssh_private_key': 'SSH_PRIVATE_KEY',
                'docker_config': 'DOCKER_AUTH',
                'db_connection_string': 'DATABASE_URL',
            }
            env_var_name = env_var_map.get(secret_type, secret_type.upper())

            # Convert to absolute path if needed
            file_path = os.path.abspath(file_path)

            # Check if file exists
            if not os.path.exists(file_path):
                return Response({'error': f'File not found: {file_path}'}, status=status.HTTP_404_NOT_FOUND)

            # Check file write permissions
            if not os.access(file_path, os.W_OK):
                return Response({'error': f'File is read-only: {file_path}'}, status=status.HTTP_403_FORBIDDEN)

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Determine replacement syntax based on file extension
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.py']:
                replacement = f'os.getenv(\'{env_var_name}\')'
            elif file_ext in ['.sh', '.bash', '.zsh', '.env']:
                replacement = f'${{{env_var_name}}}'
            elif file_ext in ['.js', '.jsx', '.ts', '.tsx']:
                replacement = f'process.env.{env_var_name}'
            elif file_ext in ['.json']:
                replacement = '""'
            else:
                replacement = f'<{env_var_name}>'

            # Replace secret in the line containing it
            lines = content.splitlines()
            new_lines = []
            replaced = False
            for line in lines:
                if secret_value in line and not replaced:
                    new_line = line.replace(secret_value, replacement, 1)
                    new_lines.append(new_line)
                    replaced = True
                else:
                    new_lines.append(line)

            if not replaced:
                return Response({'error': 'Secret not found in file (may have been already fixed)'}, status=status.HTTP_400_BAD_REQUEST)

            new_content = "\n".join(new_lines)

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # Create/update .env file
            project_root = os.path.dirname(os.path.dirname(file_path))
            env_file = os.path.join(project_root, '.env')
            env_line = f'{env_var_name}={secret_value}\n'

            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    existing = f.read()
                if env_var_name not in existing:
                    with open(env_file, 'a', encoding='utf-8') as f:
                        f.write(env_line)
            else:
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(env_line)

            # Update .gitignore
            gitignore = os.path.join(project_root, '.gitignore')
            if os.path.exists(gitignore):
                with open(gitignore, 'r', encoding='utf-8') as f:
                    gitignore_content = f.read()
                if '.env' not in gitignore_content:
                    with open(gitignore, 'a', encoding='utf-8') as f:
                        f.write('\n.env\n')
            else:
                with open(gitignore, 'w', encoding='utf-8') as f:
                    f.write('.env\n')

            # Delete the incident after remediation
            incident.delete()

            return Response({
                'status': 'remediated',
                'incident_id': incident_id,
                'env_file': env_file,
                'message': f'Secret moved to .env as {env_var_name}'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
