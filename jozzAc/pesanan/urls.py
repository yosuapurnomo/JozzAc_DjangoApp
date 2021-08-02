from django.urls import path, re_path
from .views import (pesananKhusus,
					Tracking, ClientOrder,
					ApprovalView, InvoiceView,
					InvoiceApprov, InvoiceDetail,
					InvoiceDelete, cetakInvoice, cetakReportPendapatan, cetakReportPiutang, requestReport)

app_name = 'pesanan'

urlpatterns = [

	# Admin
	path('admin/add-khusus/', pesananKhusus.as_view(), name='add_khusus'),
	path('admin/tracking/', Tracking.as_view(), name='tracking'),
	path('admin/approval/', ApprovalView.as_view(), name='approval'),
	path('admin/approval/<slug:slug>/', InvoiceApprov.as_view(), name='invoiceCreate'),
	path('admin/invoice/view/', InvoiceView.as_view(), name='invoiceView'),
	path('admin/invoice/detail/<slug:slug>', InvoiceDetail.as_view(), name='invoiceUpdate'),
	path('admin/invoice/delete/<slug:slug>', InvoiceDelete.as_view(), name='invoiceDelete'),
	path('admin/invoice/cetak/<slug:slug>', cetakInvoice.as_view(), name='createPDF'),
	path('admin/pendapatan/cetak/', cetakReportPendapatan.as_view(), name='ReportPendapatan'),
	path('admin/piutang/cetak/', cetakReportPiutang.as_view(), name='ReportPiutang'),
	path('admin/request/cetak/', requestReport.as_view(), name='ReportRequest'),

	# Client
	path('add/', ClientOrder.as_view(), name='AddOrder'),
]