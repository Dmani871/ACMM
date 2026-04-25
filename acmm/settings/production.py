from urllib.parse import urlparse

from .base import *

"""
Settings configuration for production purposes.
"""
# Ensures that no debug data is shown upon an error
DEBUG = False

APPENGINE_URL = env("APPENGINE_URL", default=None)
if APPENGINE_URL:
    # Ensure a scheme is present in the URL before it's processed.
    if not urlparse(APPENGINE_URL).scheme:
        APPENGINE_URL = f"https://{APPENGINE_URL}"

    ALLOWED_HOSTS = [urlparse(APPENGINE_URL).hostname]
    CSRF_TRUSTED_ORIGINS = [APPENGINE_URL]
else:
    raise Exception(
        "APPENGINE_URL environment variable is not set. Please set it to the URL of your deployed application."
    )

# The database configuration for production
DATABASES = {"default": env.db()}

SECRET_KEY = env("PROD_SECRET_KEY")

SALT_KEY = env("PROD_SALT_KEY")

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
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
"""
Session
"""
# Closes session once browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
