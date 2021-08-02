from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    '''
        Admin View for Account
    '''
    model = Account
    list_display = ('username', 'last_login', 'jabatan')

    readonly_fields = ('last_login',)
    search_fields = ('username',)

    fieldsets = (
        (None, {'fields': ('username','jabatan', 'password')}),
        ('Permissions', {'fields': ('is_active','is_staff', 'is_admin', 'is_superuser')}),
        ('Group', {'fields': ('groups', 'user_permissions')}),
        )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','jabatan', 'password1', 'password2', 'is_staff', 'is_admin', 'is_superuser')
            }),
        ('Group', {'fields': ('groups', 'user_permissions')}),
    )

admin.site.register(Account, AccountAdmin)

# class jabatanInLine(admin.StackedInline):
#     model = Account
#     can_delete = False
#     verbose_name_plural = 'Jabatan'

# class userAdmin(BaseUserAdmin):
#     inlines = (jabatanInLine,)

# admin.site.unregister(User)
# admin.site.register(User, userAdmin)