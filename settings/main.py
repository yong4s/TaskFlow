import sys

from .base import *

INSTALLED_APPS += [
    'django_extensions',
]

AUTH_USER_MODEL = 'accounts.User'

# Environment
TESTING_ENVIRONMENT = 'testing'
PRODUCTION_ENVIRONMENT = 'production'
STAGING_ENVIRONMENT = 'staging'
DEVELOPMENT_ENVIRONMENT = 'development'

if 'test' in sys.argv:  # noqa: SIM108
    ENVIRONMENT = TESTING_ENVIRONMENT
else:
    ENVIRONMENT = env('ENVIRONMENT')

# Testing environment optimizations
if ENVIRONMENT == TESTING_ENVIRONMENT:
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]
