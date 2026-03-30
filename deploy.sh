#!/usr/bin/env bash
set -euo pipefail

# Load env vars if .env exists
if [ -f .env ]; then
  set -a; source .env; set +a
fi

# Validate required vars
: "${AWS_ACCOUNT_ID:?}"
: "${AWS_REGION:?}"
: "${ECR_REPO_NAME:?}"
: "${IMAGE_TAG:=latest}"
: "${CONTAINER_PORT:=8080}"
: "${EB_APP_NAME:?}"
: "${EB_ENV_NAME:?}"

ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# Authenticate Docker to ECR
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

# Inject vars into Dockerrun.aws.json
envsubst < Dockerrun.aws.json > Dockerrun.aws.json.rendered
mv Dockerrun.aws.json.rendered Dockerrun.aws.json

# Deploy to Elastic Beanstalk
eb deploy "$EB_ENV_NAME" --app "$EB_APP_NAME"
