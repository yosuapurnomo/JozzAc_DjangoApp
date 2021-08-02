from django.contrib import admin
from .models import InvoiceModel, Job_OrderModel, approvalModel
from client.models import ClientModel

# Register your models here.


class InvoiceAdmin(admin.ModelAdmin):

    list_display = ('tanggal', 'Invoice', 'clientINV' , 'totalInvoice', 'statusPembayaran')
    list_filter = ('tanggal',)

    readonly_fields = ('Invoice', 'slug_Invoice', 'tanggal')
    search_fields = ('Invoice', )

admin.site.register(InvoiceModel, InvoiceAdmin)

class JOAdmin(admin.ModelAdmin):

    list_display = ('nomor_jo', 'product', 'client')

admin.site.register(Job_OrderModel, JOAdmin)

class ApprovalAdmin(admin.ModelAdmin):

    list_display = ('invoice', 'client', 'approve', 'tgl_approve',)
    list_filter = ('tgl_approve',)

    readonly_fields = ('tgl_approve', 'slug_Approv')
    search_fields = ('pesanan', )
    
admin.site.register(approvalModel, ApprovalAdmin)

