from .base import *

SECRET_KEY = "django-insecure-11rcbiu(vo0wy2u=v6=3&jr#tdp5ddb@d%gh!s%%sy)%8hy3=r"  # todo handle secret key

DEBUG = True

MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
]

INSTALLED_APPS += [
    "silk",
]

ROOT_URLCONF = "config.silky_urls"
