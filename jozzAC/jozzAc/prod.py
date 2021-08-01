from .settings import *

DEBUG = False


ALLOWED_HOSTS = [
	'*', 'http://jozacsurabaya.com:8000/', '101.50.2.224:8000'
]

STATIC_ROOT = '/home/static/'
MEDIA_ROOT = '/home/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

# '101.50.2.224:9000'
# 'jozacsurabaya.com', 'jozacsurabaya',
# 	'jozacsurabaya.com:9001', '101.50.2.224:9001',
# 	'127.0.0.1:9001', 