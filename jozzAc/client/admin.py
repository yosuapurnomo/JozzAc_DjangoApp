from django.contrib import admin
from .models import ClientModel
from pesanan.models import Job_OrderModel

# Register your models here.

class JO(admin.TabularInline):
	model = Job_OrderModel
	fields = ('product', 'jumlah_Ac', 'keterangan')

class ClientAdmin(admin.ModelAdmin):
    '''
        Admin View for Client
    '''
    inlines = [
        JO
    ]
    class Meta:
    	model = ClientModel
    	
    list_display = ('id', 'nama_Client', 'noTelp_Client', 'email_Client')
    list_filter = ('id','nama_Client')

    readonly_fields = ('slug_Client',)
    search_fields = ('noTelp_Client', 'email_Client', 'nama_Client')

admin.site.register(ClientModel, ClientAdmin)