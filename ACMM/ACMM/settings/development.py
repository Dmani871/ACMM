from .base import *
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DEV_DB_HOST'),
        'PORT': env.str('DEV_DB_PORT'),
        'USER': env.str('DEV_DB_USER'),
        'PASSWORD': env.str('DEV_DB_PASSWORD'),
        'NAME': env.str('DEV_DB_NAME'),
    }
}
