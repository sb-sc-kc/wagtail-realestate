from .base import *

DEBUG = True
SECRET_KEY = 'django-insecure-9r1y+3r(0o3ozo0#95f7gxemp42#^26d*woj=lk-vd&sz&5e(6'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

try:
    from .local import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['POSTGRES_SERVICE'],
        'PORT': os.environ['POSTGRES_PORT'],}
}
