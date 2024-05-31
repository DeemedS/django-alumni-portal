# DJANGO ALUMNI PORTAL

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
Create .env file
```
SECRET_KEY=

# PostgreSQL Credentials
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_SSLMODE=

DEBUG=

# Recaptcha
RECAPTCHA_SITE_KEY=
RECAPTCHA_SECRET_KEY=
```

## Run the Development Server
```
python manage.py runserver
```
   
