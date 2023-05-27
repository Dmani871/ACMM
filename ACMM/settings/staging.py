from .base import *

"""
Settings configuration for staging purposes.
"""

# Ensures that errors are shown with debug data
DEBUG = True

# Empty allowed hosts
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('DEV_DB_HOST'),
        'USER': "dbmanager",
        'PASSWORD': "e(&2h,hiJ,IiUiPk",
        'NAME': env.str('PROD_DB_NAME'),
    }
}

from django.db import connections
from django.db.utils import OperationalError
db_conn = connections['default']
try:
    c = db_conn.cursor()
except OperationalError:
    connected = False
else:
    connected = True
print(connected)
print(DATABASES)