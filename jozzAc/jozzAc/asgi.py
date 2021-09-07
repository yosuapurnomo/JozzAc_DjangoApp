import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
# from .wsgi import *

from django.urls import path, include, re_path
from pesanan.consumers import PesananConsumer, InvoiceConsumer
from SPK_teknisi.consumers import getSPK
from pembayaran.consumers import getPayment


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jozzAc.settings')

urlpatterns = [
	re_path(r'^pesanan/admin/tracking/(?P<id>\w+)$', PesananConsumer.as_asgi()),
	re_path(r'^pesanan/admin/invoice/view/(?P<invoice>\w+)$', InvoiceConsumer.as_asgi()),
	re_path(r'^spk/admin/list_spk/(?P<key>\w+)$', getSPK.as_asgi()),
	re_path(r'^pembayaran/admin/search/(?P<key>\w+)$', getPayment.as_asgi()),
]

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				urlpatterns
				)
			)
		)
	})

  
# import os
# import django
# from .wsgi import *
# from channels.routing import get_default_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jozzAc.settings')
# django.setup()
# application = get_default_application()