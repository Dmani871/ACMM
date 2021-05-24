import io
import os
import environ
#os.path.abspath(os.path.join(os.path.dirname(__file__),'../..', '.env'))
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)))
env_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..', '.env'))

env = environ.Env()
# If no .env has been provided, pull it from Secret Manager
if os.path.isfile(env_file):
    env.read_env(env_file)
else:
    # Create local settings if running with CI, for unit testing
    if os.getenv("TRAMPOLINE_CI", None):
        placeholder = f"SECRET_KEY=a\nGS_BUCKET_NAME=none\nDATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
        env.read_env(io.StringIO(placeholder))
    else:
        # [START cloudrun_django_secretconfig]
        import google.auth
        from google.cloud import secretmanager

        _, project = google.auth.default()

        if project:
            client = secretmanager.SecretManagerServiceClient()

            SETTINGS_NAME = os.environ.get("SETTINGS_NAME", "django_settings")
            name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
            payload = client.access_secret_version(name=name).payload.data.decode(
                "UTF-8"
            )
        env.read_env(io.StringIO(payload))
        # [END cloudrun_django_secretconfig]
