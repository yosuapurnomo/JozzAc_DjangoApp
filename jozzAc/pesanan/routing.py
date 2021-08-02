from django.urls import re_path
from .consumers import PesananConsumer, InvoiceConsumer

app_name = 'ws_pesanan'

ws_urlpatterns = [
	re_path(r'admin/tracking/(?P<id>\w+)$', PesananConsumer.as_asgi()),
	re_path(r'admin/invoice/view/(?P<invoice>\w+)$', InvoiceConsumer.as_asgi())
]