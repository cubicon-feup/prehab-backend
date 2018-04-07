# ENVIRONMENT = 'local'
ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'settings.development'

if ENVIRONMENT == 'development':
    SETTINGS_MODULE = 'settings.development'
if ENVIRONMENT == 'production':
    SETTINGS_MODULE = 'settings.production'
