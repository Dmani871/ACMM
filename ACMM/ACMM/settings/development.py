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
    }
}

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS',True)
EMAIL_PORT = os.environ.get('EMAIL_PORT',587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER','dbsoftwaresoultions@gmail.com') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD','dbsoftwaresoultions@gmail.com')

GDPR_CAN_ANONYMISE_DATABASE = False
SECURE_SSL_REDIRECT = False