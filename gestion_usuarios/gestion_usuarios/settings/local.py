from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER' : get_secret('USER'),
        'PASSWORD' : get_secret('PASSWORD'),
        'HOST' : 'localhost',
        'DATABASE_PORT' : '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    'static'
]

#creando path media
MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR,'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_secret('EMAIL')
EMAIL_HOST_PASSWORD = get_secret('PASSWORD_EMAIL')
EMAIL_PORT = 587
