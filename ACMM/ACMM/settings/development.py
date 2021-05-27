from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DEV_DB_HOST'),
        'PORT': env.str('DEV_DB_PORT'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'NAME': env.str('PROD_DB_NAME'),
    }
}
EMAIL_CONFIG = env.email_url('EMAIL_URL')
