from .base import *
import os
import dj_database_url

my_debug = os.getenv('DEBUG')
if my_debug == "False":
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ['cowrywise-backend.herokuapp.com']

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True