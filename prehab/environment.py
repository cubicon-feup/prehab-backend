# ENVIRONMENT = 'local'
ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'prehab.settings.production'

if ENVIRONMENT == 'development':
    SETTINGS_MODULE = 'prehab.settings.development'
if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'prehab.settings.production'
