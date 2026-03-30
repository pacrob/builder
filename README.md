# builder

A minimal time-tracking web app. Log tasks by name and duration; view hours grouped by day.

Built with Flask + PostgreSQL, deployed on Elastic Beanstalk (native Python platform). Merges to `main` run CI and auto-deploy if tests pass.

---

## Local Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
flask --app application run --debug
```

---

## AWS Setup

### 1 — Create an RDS PostgreSQL Instance

1. AWS Console → **RDS** → **Create database**
2. Engine: **PostgreSQL** (latest 16.x)
3. Template: **Free tier** (or Production as needed)
4. **DB instance identifier**: e.g. `timetracker-db`
5. **Master username** and **Master password**: save these — you'll need them for `DATABASE_URL`
6. **DB name** (under "Additional configuration"): e.g. `timetracker`
7. **VPC**: choose the same VPC your EB environment will use (default VPC is fine)
8. **Public access**: **No** — the app connects from within the VPC
9. Create the database. Note the **Endpoint** shown on the instance detail page.

### 2 — Configure the RDS Security Group

The RDS instance needs to accept connections from your EB instances:

1. In the RDS instance detail, click the **VPC security group**
2. **Inbound rules** → **Edit inbound rules** → **Add rule**
3. Type: **PostgreSQL** (port 5432), Source: the security group attached to your EB environment
4. Save

### 3 — Create an Elastic Beanstalk Application

1. AWS Console → **Elastic Beanstalk** → **Create application**
2. **Application name**: e.g. `timetracker`
3. **Platform**: Python, Python 3.12, Amazon Linux 2023
4. **Application code**: Sample application (you'll deploy the real code via GitHub Actions)
5. Under **Configure more options** → **Software** → **Environment properties**, add:

   | Key | Value |
   |---|---|
   | `DATABASE_URL` | `postgresql://username:password@your-rds-endpoint:5432/timetracker` |
   | `SECRET_KEY` | a long random string |
   | `APP_USERNAME` | your login username |
   | `APP_PASSWORD` | your login password |

6. Create the environment. Note the **Application name** and **Environment name**.

### 4 — Add GitHub Actions Secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key with `AWSElasticBeanstalkFullAccess` |
| `AWS_SECRET_ACCESS_KEY` | Corresponding secret key |
| `AWS_REGION` | e.g. `us-east-1` |
| `EB_APP_NAME` | EB application name from step 3 |
| `EB_ENV_NAME` | EB environment name from step 3 |

---

## CI / CD

Every push runs the test suite. Merges to `main` additionally deploy to Elastic Beanstalk — only if all tests pass.

```
push to any branch  →  pytest
merge to main       →  pytest → deploy to EB
```

---

## Running Tests

```bash
pytest --tb=short -q
```
