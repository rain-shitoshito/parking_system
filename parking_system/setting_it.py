import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-m@n=!95%c^e&z=81!@%b=8)daxw2k-%5k)8d)17cmqv0dji2dt'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'parking_system',
        'USER': 'postgres',
        'PASSWORD': 'C0degeass',
        'HOST': 'localhost',
        'POST': '5432'
    }
}
LOG_BASE_DIR = os.path.join(BASE_DIR ,'log')