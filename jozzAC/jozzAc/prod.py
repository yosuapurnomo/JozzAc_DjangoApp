from .settings import *

DEBUG = False

STATIC_URL = '/static/'


ALLOWED_HOSTS = [
	'jozacsurabaya.com', 'jozacsurabaya',
	'jozacsurabaya.com:9001', '101.50.2.224:9001',
	'127.0.0.1:9001', '*'
]

STATIC_ROOT = '/root/demo/www/public/static'

# '101.50.2.224:9000'