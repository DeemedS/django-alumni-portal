# DJANGO ALUMNI PORTAL

## View live website at https://pupalumniportal.com

## Table of Contents
- Installation
- Configuration


## Installation
### Prerequisites
- Python (>= 3.7)
- Django (>= 3.0)
- Virtualenv

### Steps
1. Clone the repository:
```
git clone https://github.com/DeemedS/django-alumni-portal.git
cd django-alumni-portal
```
2. Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up the database:
```
python manage.py migrate
```
5. Create a superuser:
```
python manage.py createsuperuser
```
6. Collect static files:
```
python manage.py collectstatic
```
## Configuration
Create .env file (see .env.example)
```
SECRET_KEY=

# PostgreSQL Credentials
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
DB_SSLMODE=

DEBUG=

# allowed hosts
ALLOWED_HOSTS=

# Recaptcha
RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
```

## Run the Development Server
```
python manage.py runserver
```
   
