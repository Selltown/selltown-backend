from .base import *

DEBUG = False

LOGGING["loggers"]["apps"]["level"] = "INFO"

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True
