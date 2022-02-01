import environ
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Gets the file location of the .env file
env_file = Path(ROOT_DIR,".env")

# Create a new environment
env = environ.Env()

# Take environment variables from .env file
env.read_env(env_file)
