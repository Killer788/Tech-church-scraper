# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!wo^-)v1drdsu1t4py0sfs==gtj(^!og0l5vkmj_f%%@pb5k6&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Celery Configuration Options
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
