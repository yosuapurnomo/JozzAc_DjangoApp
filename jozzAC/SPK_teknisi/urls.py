from django.urls import path, include, re_path
from .views import (SPK_Create,
					SPK_InvoiceView,
					SPK_Progress_List,
					searchSPK,
					SPK_Update,
					list_SPK_teknisi, SPK_Delete, cetakPDF, SPK_UpdateStatus, cetakReport)

app_name = 'spk'

urlpatterns = [
	path('admin/create/<slug:slug>/', SPK_Create.as_view(), name='create'),
	path('admin/update/<slug:slug>/', SPK_Update.as_view(), name='update'),
	path('admin/delete/<slug:slug>/', SPK_Delete.as_view(), name='delete'),
	path('admin/cetak/<slug:slug>/', cetakPDF.as_view(), name='cetakPDF'),
	path('admin/invocie_view/', SPK_InvoiceView.as_view(), name='invoiceView'),
	path('admin/OnProgress/', SPK_Progress_List.as_view(), name='OnProgress'),
	path('admin/list_spk/', searchSPK.as_view(), name='listSPK'),
	path('admin/cetak/report', cetakReport.as_view(), name='cetakReport'),
	
	path('admin/teknisi_spk/', list_SPK_teknisi.as_view(), name='teknisiSPK'),
	path('admin/teknisi_spk/<slug:slug>', SPK_UpdateStatus.as_view(), name='updateStatus'),
]