import os
from django.core.wsgi import get_wsgi_application
from .settings.env_config import env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACMM.settings.development')

if env('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = env('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()
