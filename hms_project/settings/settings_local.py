from hms_project.settings import *



DATABASES['default'].update({
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'production_db',
    'USER': 'db_user',
    'PASSWORD': 'db_password',
    'HOST': 'db_host',
    'PORT': 'db_port',
})

# Disable debug mode
DEBUG = False

# Add production-specific middleware
MIDDLEWARE += [
    # Production-specific middleware...
]

# Add production-specific authentication backends
AUTHENTICATION_BACKENDS += [
    # Production-specific authentication backends...
]

# Update logging configuration
LOGGING.update({
    # Production-specific logging configuration...
})
