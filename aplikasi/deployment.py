import os
from.settings import *
from .settings import BASE_DIR
import base64
import json


SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False



# Ambil dari environment variable
service_account_b64 = os.getenv("SERVICE_ACCOUNT_JSON")

if service_account_b64:
    # Decode base64 dan buat file JSON
    service_account_json = base64.b64decode(service_account_b64).decode("utf-8")
    service_account_path = "aplikasi/serviceAccountKey.json"
    
    # Pastikan folder ada
    os.makedirs(os.path.dirname(service_account_path), exist_ok=True)
    
    # Simpan ke file
    with open(service_account_path, "w") as f:
        f.write(service_account_json)
else:
    raise ValueError("Environment variable SERVICE_ACCOUNT_JSON tidak ditemukan!")

# WhiteNoise configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] 

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


conn_str = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}