from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from .views import dasboardList, dasboardAdmin, landingPage

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('admin/', dasboardAdmin.as_view(), name='dasboardAdmin'),
    path('admin/', include('account.urls', namespace='account')),
    path('', dasboardList.as_view(), name='dasboard'),
    path('success/', landingPage.as_view(), name='landingPage'),
    path('product/', include('product.urls', namespace='product')),
    path('pesanan/', include('pesanan.urls', namespace='pesanan')),
    path('spk/', include('SPK_teknisi.urls', namespace='spk')),
    path('pembayaran/', include('pembayaran.urls', namespace='pembayaran')),
    path('content/', include('eventContent.urls', namespace='eventContent')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'jozzAc.views.handle404'

handler500 = 'jozzAc.views.handle404'