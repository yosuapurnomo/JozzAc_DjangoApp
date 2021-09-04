from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path, include, re_path
from pesanan.consumers import PesananConsumer, InvoiceConsumer
from SPK_teknisi.consumers import getSPK
from pembayaran.consumers import getPayment

urlpatterns = [
	re_path(r'^pesanan/admin/tracking/(?P<id>\w+)$', PesananConsumer.as_asgi()),
	re_path(r'^pesanan/admin/invoice/view/(?P<invoice>\w+)$', InvoiceConsumer.as_asgi()),
	re_path(r'^spk/admin/list_spk/(?P<key>\w+)$', getSPK.as_asgi()),
	re_path(r'^pembayaran/admin/search/(?P<key>\w+)$', getPayment.as_asgi()),
]

application = ProtocolTypeRouter({
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				urlpatterns
				)
			)
		)
	})