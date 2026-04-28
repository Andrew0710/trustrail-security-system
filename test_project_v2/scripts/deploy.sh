#!/bin/bash
# Deployment script - contains secrets (bad practice)

# AWS Credentials (should be in env vars, not here!)
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
export AWS_SECRET_ACCESS_KEY="${AZURE_TOKEN}"
export AWS_DEFAULT_REGION="us-east-1"

# Deploy to EC2
echo "Deploying to production..."
aws s3 sync ./ s3://my-bucket/ --delete