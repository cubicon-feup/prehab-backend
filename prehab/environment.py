import os.path

# ENVIRONMENT = 'local'
ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'prehab.settings.development'

if os.path.isfile('prehab/settings/production.py'):
    SETTINGS_MODULE = 'prehab.settings.production'
