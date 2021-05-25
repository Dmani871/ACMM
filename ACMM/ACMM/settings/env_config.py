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
    # [START cloudrun_django_secretconfig]
    import google.auth
    from google.cloud import secretmanager as sm
    SETTINGS_NAME = "application_settings"
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    env.read_env(io.StringIO(payload))
    # [END cloudrun_django_secretconfig]
