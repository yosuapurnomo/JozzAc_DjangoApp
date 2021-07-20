from django.contrib import admin
from .models import eventContentModel as event

# Register your models here.
class eventAdmin(admin.ModelAdmin):
    '''
        Admin View for event
    '''
    list_display = ('nama_Content', 'admin',)
    list_filter = ('tgl_upload',)

    readonly_fields = ('tgl_upload','slug_Content')
    search_fields = ('nama_Content',)

admin.site.register(event, eventAdmin)