from .settings import *

DEBUG = False


ALLOWED_HOSTS = [
	'www.jozacsurabaya.com', 'jozacsurabaya.com', 'jozacsurabaya'
]

STATIC_ROOT = '/root/demo/www/public/static'
MEDIA_ROOT = '/root/demo/www/public/media'

# '101.50.2.224:9000'
# 'jozacsurabaya.com', 'jozacsurabaya',
# 	'jozacsurabaya.com:9001', '101.50.2.224:9001',
# 	'127.0.0.1:9001', 