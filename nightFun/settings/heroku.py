import environ

from nightFun.settings.base import *

env = environ.Env()

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ORIGIN_ALLOW_ALL = True
DATABASES = {
    "default": env.db(),
}