from .base import *

"""
Settings configuration for development purposes.
"""
# Ensures that errors are shown with debug data
DEBUG = True

# Allowed hosts for development
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# The database configuration for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("DEV_DB_HOST"),
        "PORT": env.str("DEV_DB_PORT"),
        "USER": env.str("DEV_DB_USER"),
        "PASSWORD": env.str("DEV_DB_PASSWORD"),
        "NAME": env.str("DEV_DB_NAME"),
    }
}

SECRET_KEY = env("DEV_SECRET_KEY")

SALT_KEY = env("DEV_SALT_KEY")
