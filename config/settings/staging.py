from .base import *

DEBUG = False

LOGGING["loggers"]["apps"]["level"] = "INFO"

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_CONTENT_TYPE_NOSNIFF = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CORS_ALLOW_CREDENTIALS = True
