# Settings when deploying to amazon
from settings import INSTALLED_APPS, STATICFILES_DIRS

INSTALLED_APPS += (
    'collectfast',
)

STATICFILES_DIRS = (
    'client/static',
)

DEBUG = False
DEBUG_TOOLBAR_PATCH_SETTINGS = TEMPLATE_DEBUG = DEBUG
