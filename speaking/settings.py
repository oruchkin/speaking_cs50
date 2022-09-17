from split_settings.tools import include
from pathlib import Path
import os

include(
    'components/auth_password_validators.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/tempates.py',
    'components/monkey_patch.py',
) 

ALLOWED_HOSTS = ["*"]
DEBUG = True


CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'speaking.urls'
WSGI_APPLICATION = 'speaking.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
AUTH_USER_MODEL = 'spapp.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECRET_KEY = 'django-insecure-$-x4*2nws4s8@x-jj)g@q)^16k484&7uvske-^^hm&jsty5eg6'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')