from .base import *
import os

DEBUG = False

# EC2 퍼블릭 IP 또는 도메인
ALLOWED_HOSTS = ["13.209.97.126", "api.yourdomain.com"]

# HTTPS 적용 전 임시값 (인증서/도메인 연결 후 True/HSTS 활성화)
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = [
    "http://52.79.169.55",
    "https://52.79.169.55",
    # "https://api.yourdomain.com",
]

# ✅ Database (환경변수 기반, PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "ViralMarketing"),
        "USER": os.getenv("DB_USER", "admin"),
        "PASSWORD": os.getenv("DB_PASSWORD", "1234"),
        "HOST": os.getenv("DB_HOST", "localhost"),   # 도커면 db, EC2면 localhost/RDS endpoint
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ✅ 운영 로그 (터미널 출력)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
