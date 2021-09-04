from .settings import *

DEBUG = True

ALLOWED_HOSTS = [
	'www.jozacsurabaya.com', 'jozacsurabaya.com',
	 'jozacsurabaya', '*'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')