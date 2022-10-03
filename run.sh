#!/usr/bin bash

echo "[setup] Apply DB migrations"
python manage.py migrate

echo "[setup] Create INE staff user"
python manage.py createstaffuser

echo "[setup] Run server"
python manage.py runserver 0.0.0.0:8000
