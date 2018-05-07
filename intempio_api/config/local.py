import logging
import os

from .common import Common

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose', 'nplusone.ext.django', 'debug_toolbar')
    MIDDLEWARE = Common.MIDDLEWARE
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', 'nplusone.ext.django.NPlusOneMiddleware',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=intempio_api'
    ]

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ADMIN_URL = os.getenv('ADMIN_URL', 'http://localhost:8000')
    ENVIRONMENT_NAME = 'LOCAL'
    NPLUSONE_LOGGER = logging.getLogger('nplusone')
    NPLUSONE_LOG_LEVEL = logging.WARN
    INTERNAL_IPS = '127.0.0.1'
