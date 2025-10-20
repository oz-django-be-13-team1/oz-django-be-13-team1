from .base import *
from dotenv import load_dotenv

# load_dotenv(BASE_DIR/"envs/.env")

ALLOWED_HOSTS = ["13.209.97.126", "0.0.0.0"]

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", default="db"),
            "PORT": os.getenv("POSTGRES_PORT", default="5432"),
        }
    }

DEBUG = False