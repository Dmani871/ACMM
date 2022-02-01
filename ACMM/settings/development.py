from .base import *

"""
Settings configuration for development purposes.
"""

# Ensures that errors are shown with debug data
DEBUG = True

# Empty allowed hosts
ALLOWED_HOSTS = []

# The database configuration for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DEV_DB_HOST'),
        'PORT': env.str('DEV_DB_PORT'),
        'USER': env.str('DEV_DB_USER'),
        'PASSWORD': env.str('DEV_DB_PASSWORD'),
        'NAME': env.str('DEV_DB_NAME'),
    }
}
