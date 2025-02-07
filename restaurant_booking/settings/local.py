from .base import *

ENV_SETTINGS = "LOCAL"

# Django Debug Toolbar
# -----------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]
