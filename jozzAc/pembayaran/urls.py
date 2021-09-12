from django.urls import path, re_path
from .views import ListPayment, create, searchPayment, UpdatePayment, createPDF, getPaymentView

app_name = 'pembayaran'

urlpatterns = [
	path('admin/list/', ListPayment.as_view(), name='list'),
	path('admin/search/', searchPayment.as_view(), name='search'),
	path('admin/search/getView/', getPaymentView.as_view()),
	path('admin/detail/<slug:slug>/', UpdatePayment.as_view(), name='update'),
	path('admin/delete/<slug:slug>/', UpdatePayment.as_view(), name='delete'),
	path('admin/create/<slug:slug>/', create.as_view(), name='create'),
	path('admin/cetak/<slug:slug>/', createPDF.as_view(), name='cetak'),
]