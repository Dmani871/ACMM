from .base import *
DEBUG = False

ALLOWED_HOSTS = ['acmm-mentorship.ew.r.appspot.com']
DATABASES = { 
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('PROD_DB_HOST'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'NAME': env.str('PROD_DB_NAME'),
    }
}
EMAIL_CONFIG = env.email_url('EMAIL_URL')
# SSL settings
SECURE_SSL_REDIRECT = True
# CSRF settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
#XSS settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#HSTS settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
#Session
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_AGE=3600


