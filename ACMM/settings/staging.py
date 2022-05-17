from .base import *

"""
Settings configuration for staging purposes.
"""

# Ensures that errors are shown with debug data
DEBUG = True

# Empty allowed hosts
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DEV_DB_HOST'),
        'USER': env.str('PROD_DB_USER'),
        'PASSWORD': env.str('PROD_DB_PASSWORD'),
        'NAME': env.str('PROD_DB_NAME'),
    }
}
