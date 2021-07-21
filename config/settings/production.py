from .base import *
import os
# import dj_database_url
import django_heroku


my_debug = os.getenv('DEBUG')
if my_debug == "False":
    DEBUG = False
else:
    DEBUG = True


ALLOWED_HOSTS = ['cowrywise-backend.herokuapp.com']

SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

django_heroku.settings(locals())