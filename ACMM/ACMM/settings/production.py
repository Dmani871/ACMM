from .base import *
import dj_database_url
DEBUG = False
ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', ''),
    },
    'gdpr_log': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'gdpr-log.sqlite3'),
    },
}
DATABASE_ROUTERS = ['gdpr_assist.routers.EventLogRouter']
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS',True)
EMAIL_PORT = os.environ.get('EMAIL_PORT',587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','dbsoftwaresoultions@gmail.com') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','dbsoftwaresoultions@gmail.com')
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
# CSP settings
CSP_DEFAULT_SRC = ("'none'", )
CSP_STYLE_SRC = ("'self'", )
CSP_SCRIPT_SRC = ("'self'", )
CSP_IMG_SRC = ("'self'", )
CSP_FONT_SRC = ("'self'", )
#GDPR
GDPR_CAN_ANONYMISE_DATABASE = True
#Session
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_AGE=3600
