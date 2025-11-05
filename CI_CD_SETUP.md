# CI/CD Setup for AWS Elastic Beanstalk Deployment

## Branch: `ci`

## Overview

This document describes the GitHub Actions CI/CD workflow that automatically deploys the Django application to AWS Elastic Beanstalk when code is pushed to the `main` branch.

## Changes Made

### 1. Created GitHub Actions Workflow
**File: `.github/workflows/deploy.yml`**

This workflow file was created based on the existing `django.yml` with the following enhancements:

#### ✨ New Features Added:
- **Dependency Installation**: Added `pip install -r requirements.txt` to install application dependencies
- **Pip Caching**: Enabled pip cache for faster subsequent builds
- **Pre-deployment Django Checks**: Runs `python manage.py check --deploy` to catch issues before deployment
- **Better Logging**: Enhanced output messages and status checks
- **Versioned Deployments**: Uses GitHub run number and commit SHA for deployment labels
- **Post-deployment Health Check**: Monitors environment health after deployment

#### 🔧 Workflow Steps:

1. **Checkout Repository** - Gets the latest code from GitHub
2. **Set up Python 3.12** - Configures Python environment with caching
3. **Install Application Dependencies** - Installs from `requirements.txt`
4. **Run Django Checks** - Validates Django configuration with production settings
5. **Install AWS Tools** - Installs EB CLI and AWS CLI
6. **Configure AWS Credentials** - Sets up AWS authentication from secrets
7. **Verify AWS Identity** - Debug step to confirm AWS configuration
8. **Check EB Configuration** - Verifies `.elasticbeanstalk` directory exists
9. **Deploy to Elastic Beanstalk** - Executes `eb deploy` to `django-env`
10. **Health Check** - Monitors deployment health status

### 2. Existing File: `django.yml`
The original `django.yml` in the root directory should be kept for reference or removed to avoid confusion. The new workflow in `.github/workflows/deploy.yml` supersedes it.

## Required GitHub Secrets

To enable this workflow, you must configure the following secrets in your GitHub repository:

### Setting Up Secrets:
1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add each of the following:

### Required Secrets:

| Secret Name | Description | How to Get It |
|------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key ID | Create in AWS IAM Console |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret access key | Created with the access key |
| `DJANGO_SECRET_KEY` | Django secret key for production | Generate using Python command below |

### Generating Django Secret Key:

Run this command to generate a secure secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output and add it as the `DJANGO_SECRET_KEY` secret in GitHub.

### AWS IAM Permissions Required:

The AWS IAM user should have the following permissions:
- `elasticbeanstalk:*`
- `ec2:*`
- `ecs:*`
- `s3:*`
- `cloudformation:*`
- `autoscaling:*`
- `elasticloadbalancing:*`
- `rds:*` (if using RDS)

Alternatively, use the AWS managed policy: `AdministratorAccess-AWSElasticBeanstalk`

## Workflow Triggers

The workflow runs automatically in two scenarios:

1. **Automatic**: When code is pushed to the `main` branch
2. **Manual**: Via "Actions" tab → "Deploy to Elastic Beanstalk" → "Run workflow"

## Local Testing Before Deployment

Before pushing to `main`, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run Django checks with production settings
python manage.py check --deploy

# Set production environment variables for testing
export DJANGO_SECRET_KEY="your-secret-key"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="your-domain.com"

# Run the development server
python manage.py runserver
```

## Deployment Process

### What Happens When You Push to Main:

1. GitHub Actions workflow is triggered
2. Code is checked out and Python environment is set up
3. Dependencies are installed from `requirements.txt`
4. Django configuration is validated
5. AWS credentials are configured
6. Code is deployed to Elastic Beanstalk environment `django-env`
7. Deployment health is monitored

### Monitoring Deployment:

- **GitHub Actions**: Repository → Actions tab → Click on the running workflow
- **AWS Console**: Elastic Beanstalk → Environments → `django-env` → Events
- **EB CLI**: Run `eb status django-env` or `eb health django-env`

## Environment Variables in Elastic Beanstalk

Make sure these environment variables are configured in your EB environment:

1. Go to: **Elastic Beanstalk Console** → **django-env** → **Configuration** → **Software**
2. Under **Environment properties**, add:

| Variable Name | Value |
|--------------|-------|
| `DJANGO_SECRET_KEY` | Your production secret key (same as GitHub secret) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Your domain(s), comma-separated |

## Rollback Strategy

If a deployment fails or causes issues:

### Option 1: Rollback via AWS Console
1. Go to Elastic Beanstalk Console
2. Select your environment
3. Click "Actions" → "Restore environment"
4. Select a previous application version

### Option 2: Rollback via EB CLI
```bash
eb deploy django-env --version <previous-version-label>
```

### Option 3: Revert Git Commit
```bash
git revert <commit-sha>
git push origin main
```
This triggers a new deployment with the reverted code.

## Troubleshooting

### Deployment Fails with "Environment not found"
- Check that `.elasticbeanstalk/config.yml` exists in your repository
- Verify the environment name is `django-env`
- Ensure AWS credentials have proper permissions

### Django Check Fails
- Review the error message in the GitHub Actions log
- Test locally with: `python manage.py check --deploy`
- Ensure all required environment variables are set

### AWS Authentication Fails
- Verify GitHub secrets are correctly set
- Check IAM user permissions in AWS Console
- Ensure access keys are active and not expired

### Deployment Times Out
- Default timeout is 30 minutes
- Check Elastic Beanstalk events in AWS Console
- Verify application is starting correctly by checking EB logs

## Best Practices

1. **Never commit secrets** to the repository - use GitHub Secrets
2. **Test locally** before pushing to main
3. **Use feature branches** for development, merge to main when ready
4. **Monitor deployments** via GitHub Actions and AWS Console
5. **Keep dependencies updated** in `requirements.txt`
6. **Review EB logs** regularly for issues
7. **Set up Slack/email notifications** for deployment status (optional)

## Viewing Logs

### GitHub Actions Logs:
- Repository → Actions → Select workflow run → Expand steps

### Elastic Beanstalk Logs:
```bash
# Via EB CLI
eb logs django-env

# Or download from AWS Console
# EB Console → Environments → django-env → Logs → Request Logs
```

## Next Steps

1. ✅ Review and test the workflow configuration
2. ✅ Add required GitHub Secrets
3. ✅ Verify EB environment variables are set
4. ✅ Test deployment by pushing to main
5. ⏭️ Consider adding automated tests before deployment
6. ⏭️ Set up database backups
7. ⏭️ Configure custom domain and SSL certificate
8. ⏭️ Set up monitoring and alerting (CloudWatch, Sentry, etc.)

## Differences from Original `django.yml`

| Feature | Original `django.yml` | New `.github/workflows/deploy.yml` |
|---------|---------------------|----------------------------------|
| Location | Root directory | `.github/workflows/` (proper location) |
| Dependencies | Not installed | ✅ Installs from `requirements.txt` |
| Pre-deployment Checks | None | ✅ Runs Django checks |
| Pip Caching | No | ✅ Enabled for faster builds |
| Deployment Labels | Simple SHA | ✅ Versioned with run number + SHA |
| Health Check | No | ✅ Post-deployment health monitoring |
| Error Handling | Basic | ✅ Enhanced with status checks |

## Support and Resources

- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- **AWS EB CLI**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **EB Python Platform**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

