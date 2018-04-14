from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# INSTALLED_APPS.append('debug_toolbar')
#
# MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

JWT_SECRET = 'test'
SECRET_KEY = 'k&b05=-bsxwn$7$z8_$_d^d&n0vb)t4t#xmyd3y2y268djnnqs'
