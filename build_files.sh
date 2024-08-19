pip3 install -r requirements.txt --noinput
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
