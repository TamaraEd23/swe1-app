# SWE1 Django App

[![Django CI/CD](https://github.com/TamaraEd23/swe1-app/actions/workflows/deploy.yml/badge.svg)](https://github.com/TamaraEd23/swe1-app/actions/workflows/deploy.yml)

A Django polling application with automated CI/CD deployment to AWS Elastic Beanstalk.

## Features

- 📊 Polling system for creating and voting on polls
- 🔄 Automated testing with Black, Flake8, and coverage
- 🚀 Continuous deployment to AWS Elastic Beanstalk
- 🔒 Production-ready security settings
- ✅ Root URL redirect to `/polls/`

## Tech Stack

- **Framework**: Django 5.0
- **Python**: 3.10, 3.11, 3.12
- **Deployment**: AWS Elastic Beanstalk
- **CI/CD**: GitHub Actions
- **Code Quality**: Black, Flake8, Coverage

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='polls' manage.py test
coverage report

# Check code formatting
black --check .
flake8 .
```

## Deployment

The application automatically deploys to AWS Elastic Beanstalk when code is pushed to the `main` branch.

### Environment Variables

Set these in your Elastic Beanstalk environment:

- `DJANGO_SECRET_KEY`: Your production secret key
- `DJANGO_DEBUG`: Set to `False` for production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Manual Deployment

```bash
# Check environment status
eb status

# Deploy manually
eb deploy django-env
```

## Project Structure

```
swe1-app/
├── mysite/          # Django project settings
├── polls/           # Polls application
├── .github/         # GitHub Actions workflows
├── static/          # Static files
├── requirements.txt # Python dependencies
└── manage.py        # Django management script
```

## CI/CD Pipeline

The CI/CD pipeline runs on every push to `main`:

1. **Test** (Python 3.10)
   - Code formatting check (Black)
   - Linting (Flake8)
   - Unit tests with coverage
   - Coverage reporting to Coveralls

2. **Deploy** (Only on `main` push)
   - Initialize EB CLI
   - Deploy to `django-env`
   - Automated health checks

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass locally
4. Create a pull request

## License

This project is for educational purposes.

