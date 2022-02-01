import os
from django.core.wsgi import get_wsgi_application
print(os.getenv('DJANGO_SETTINGS_MODULE', 'ACMM.settings.development'))
os.environ['DJANGO_SETTINGS_MODULE']=os.getenv('DJANGO_SETTINGS_MODULE', 'ACMM.settings.development')
application = get_wsgi_application()
