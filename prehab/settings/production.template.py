from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'xxxxxxxx',
        'USER': 'xxxxxxxx',
        'PASSWORD': 'xxxxxxxxxxxx',
        'HOST': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',  # Or an IP Address that your DB is hosted on
        'PORT': '5432'
    }
}

JWT_SECRET = 'yyyyyy'
