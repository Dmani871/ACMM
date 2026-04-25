import os

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


LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    # Define where logs go
    "handlers": {
        # Write matching logs to file with rotation
        "matching_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "matching.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
        },
    },
    "loggers": {
        # Matching algorithm logger
        "mentorship.matching": {
            "handlers": ["matching_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
