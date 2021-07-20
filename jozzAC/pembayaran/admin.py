from django.contrib import admin
from .models import pembayaranModel

# Register your models here.
class PembayaranAdmin(admin.ModelAdmin):
    '''
        Admin View for Pesanan
    '''
    list_display = ('tgl_input', 'no_pembayaran','invoice', 'jumlah', 'tgl_pembayaran')
    list_filter = ('no_pembayaran',)

    readonly_fields = ('tgl_input', 'slug_pembayaran')
    search_fields = ('no_pembayaran', )
admin.site.register(pembayaranModel, PembayaranAdmin)