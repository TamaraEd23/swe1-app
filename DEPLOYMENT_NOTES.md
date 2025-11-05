# Deployment Notes - Root URL Fix & Production Security

## Branch: `fix/root-url-prod`

## Changes Made

### 1. Fixed Root URL (Django 404)
**File: `mysite/urls.py`**
- Added redirect from root path `/` to `/polls/`
- Imported `RedirectView` from `django.views.generic.base`
- The redirect is non-permanent (HTTP 302) to allow flexibility in the future

### 2. Production-Safe Settings
**File: `mysite/settings.py`**

#### Environment Variables
The following settings now read from environment variables with safe defaults:

- **`SECRET_KEY`**: Reads from `DJANGO_SECRET_KEY` environment variable
  - Falls back to the existing key for local development only
  - **⚠️ IMPORTANT**: Set a new secret key in production!

- **`DEBUG`**: Reads from `DJANGO_DEBUG` environment variable
  - Defaults to `False` (production-safe)
  - Must explicitly set to "True" (string) to enable debug mode

- **`ALLOWED_HOSTS`**: Reads from `DJANGO_ALLOWED_HOSTS` environment variable
  - Accepts comma-separated list of domains
  - Falls back to the existing Elastic Beanstalk domain

#### Security Headers (Production)
Added the following security settings that automatically activate in production (when `DEBUG=False`):

1. **HTTPS/SSL Enforcement**
   - `SECURE_SSL_REDIRECT`: Redirects all HTTP traffic to HTTPS
   - `SESSION_COOKIE_SECURE`: Ensures session cookies are only sent over HTTPS
   - `CSRF_COOKIE_SECURE`: Ensures CSRF cookies are only sent over HTTPS

2. **HSTS (HTTP Strict Transport Security)**
   - `SECURE_HSTS_SECONDS`: Set to 1 year (31536000 seconds)
   - `SECURE_HSTS_INCLUDE_SUBDOMAINS`: Applies HSTS to all subdomains
   - `SECURE_HSTS_PRELOAD`: Allows inclusion in browser HSTS preload lists

3. **Additional Security Headers**
   - `SECURE_CONTENT_TYPE_NOSNIFF`: Prevents MIME type sniffing
   - `SECURE_BROWSER_XSS_FILTER`: Enables browser XSS filtering
   - `X_FRAME_OPTIONS`: Set to "DENY" to prevent clickjacking

4. **AWS Elastic Beanstalk / Load Balancer Support**
   - `SECURE_PROXY_SSL_HEADER`: Properly detects HTTPS through load balancers

## Production Deployment Checklist

### Required Environment Variables

Set these environment variables in your production environment:

```bash
# Generate a new secret key using:
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
DJANGO_SECRET_KEY=<your-new-secret-key>

# Set to False for production (this is the default)
DJANGO_DEBUG=False

# Add your production domains (comma-separated)
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,django-env.eba-xmagzwfs.us-west-2.elasticbeanstalk.com
```

### AWS Elastic Beanstalk Deployment

If deploying to AWS Elastic Beanstalk, set environment variables in the EB console:

1. Go to Configuration → Software → Environment properties
2. Add the following:
   - `DJANGO_SECRET_KEY`: Your generated secret key
   - `DJANGO_DEBUG`: False (or leave unset, defaults to False)
   - `DJANGO_ALLOWED_HOSTS`: Your comma-separated list of allowed hosts

### Verification

After deployment:
1. Visit the root URL `/` - should redirect to `/polls/`
2. Check that all pages load over HTTPS
3. Verify security headers using: https://securityheaders.com/
4. Run Django security check: `python manage.py check --deploy`

## Testing Locally

To test the production settings locally:

```bash
# Set environment variables (PowerShell)
$env:DJANGO_SECRET_KEY="your-test-key"
$env:DJANGO_DEBUG="False"
$env:DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"

# Run the server
python manage.py runserver
```

Note: When `DEBUG=False`, you'll need to properly configure static files serving for local testing.

## Rollback Plan

If issues occur, you can quickly rollback by:
```bash
git checkout main
```

Or temporarily enable debug mode:
```bash
# Set environment variable
DJANGO_DEBUG=True

# Restart your application server
```

## Security Improvements Summary

✅ Secret key moved to environment variable
✅ Debug mode disabled by default
✅ HTTPS enforced in production
✅ Secure cookies enabled
✅ HSTS enabled with 1-year duration
✅ XSS and clickjacking protections enabled
✅ Content type sniffing prevention
✅ Load balancer SSL detection configured

## Next Steps

1. **Generate and set a new `DJANGO_SECRET_KEY` in production**
2. Test the root URL redirect
3. Run `python manage.py check --deploy` in production environment
4. Consider setting up a proper database (PostgreSQL/MySQL) for production
5. Configure static files serving (e.g., using WhiteNoise or S3)

