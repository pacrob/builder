# builder

Deploy a Docker image from AWS ECR to Elastic Beanstalk.

## Setup

1. Copy `.env.example` to `.env` and fill in your values:
   ```
   cp .env.example .env
   ```

2. Ensure you have the required CLIs installed:
   - [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
   - [EB CLI](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)
   - `envsubst` (part of `gettext`)

3. Run the deploy script:
   ```
   ./deploy.sh
   ```

## Configuration

| Variable | Description |
|---|---|
| `AWS_ACCOUNT_ID` | Your 12-digit AWS account ID |
| `AWS_REGION` | AWS region (e.g. `us-east-1`) |
| `ECR_REPO_NAME` | ECR repository name |
| `IMAGE_TAG` | Image tag to deploy (default: `latest`) |
| `CONTAINER_PORT` | Port the container listens on (default: `8080`) |
| `EB_APP_NAME` | Elastic Beanstalk application name |
| `EB_ENV_NAME` | Elastic Beanstalk environment name |
