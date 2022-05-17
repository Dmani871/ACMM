from .base import *
from urllib.parse import urlparse
"""
Settings configuration for production purposes.
"""
# Ensures that no debug data is shown upon an error
DEBUG = False

APPENGINE_URL = env("APPENGINE_URL", default=None)
ALLOWED_HOSTS = ["acmm-mentorship-app-350411.nw.r.appspot.com"]

# the database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env.str('PROD_DB_HOST'),
        'USER': env.str('PROD_DB_USER'),
        'PASSWORD': env.str('PROD_DB_PASSWORD'),
        'NAME': env.str('PROD_DB_NAME'),
    }
}

"""
SSL settings
"""
# Redirects any HTTP connections to HTTPS
SECURE_SSL_REDIRECT = True
"""
CSRF settings
"""
# Ensures that secure cookies are used for the session cookie so cookie only sent over HTTPS
SESSION_COOKIE_SECURE = True
# Instructs browser to only send cookies over HTTPS connections
CSRF_COOKIE_SECURE = True
# Makes it difficult for cross-site scripting
CSRF_COOKIE_HTTPONLY = True
"""
XSS settings
"""
# Ensures pages will not be served with a XSS-Protection header to prevent against X-XSS filtering
SECURE_BROWSER_XSS_FILTER = True
# Prevents the browser from identifying content types incorrectly
SECURE_CONTENT_TYPE_NOSNIFF = True
"""
HSTS settings
"""
# Reduces exposure to SSL-stripping man-in-the-middle (MITM) attacks
SECURE_HSTS_SECONDS = 31536000
# Ensures all subdomains of domains should be served exclusively via SSL
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Prevents preload
SECURE_HSTS_PRELOAD = True
"""
Session
"""
# Closes session once browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
