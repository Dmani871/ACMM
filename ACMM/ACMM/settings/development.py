from .base import *
DEBUG = True
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


EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS',True)
EMAIL_PORT = os.environ.get('EMAIL_PORT',587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','dbsoftwaresoultions@gmail.com') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','dbsoftwaresoultions@gmail.com')

GDPR_CAN_ANONYMISE_DATABASE = False