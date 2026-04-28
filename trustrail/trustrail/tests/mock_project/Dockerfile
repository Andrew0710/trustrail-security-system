FROM python:3.9
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
# Docker auth config (should not be here!)
{"auths":{"registry.example.com":{"auth":"dXNlcjpwYXNzd29yZA=="}}}