from .base import *

"""
Settings configuration for production purposes.
"""
# Ensures that no debug data is shown upon an error
DEBUG = False

# The database configuration for production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("PROD_DB_HOST"),
        "USER": env.str("PROD_DB_USER"),
        "PASSWORD": env.str("PROD_DB_PASSWORD"),
        "NAME": env.str("PROD_DB_NAME"),
    }
}

SECRET_KEY = env("PROD_SECRET_KEY")

SALT_KEY = env("PROD_SALT_KEY")
