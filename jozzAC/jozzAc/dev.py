from .settings import *

DEBUG = True

ALLOWED_HOSTS = [
	'www.jozacsurabaya.com', 'jozacsurabaya.com', 'jozacsurabaya'
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]