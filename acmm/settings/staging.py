from .base import *

"""
Settings configuration for staging purposes.
"""
# Ensures that no debug data is shown upon an error
DEBUG = False

# Allowed hosts for staging
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# The database configuration for staging
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.str("STAG_DB_HOST"),
        "USER": env.str("STAG_DB_USER"),
        "PASSWORD": env.str("STAG_DB_PASSWORD"),
        "NAME": env.str("STAG_DB_NAME"),
    }
}
SECRET_KEY = env("STAG_SECRET_KEY")

SALT_KEY = env("STAG_SALT_KEY")
