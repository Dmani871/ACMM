from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default': env.db()
}
EMAIL_CONFIG = env.email_url('EMAIL_URL')
SECURE_SSL_REDIRECT = False
