# prod(EC2) 환경 전용 설정
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
    "http://13.209.97.126",
    "https://13.209.97.126",
    # "https://api.yourdomain.com",
]

# Database → 환경변수로 주입 (RDS/도커 모두 호환)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# 운영 로깅
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
