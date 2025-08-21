from django.contrib import admin

from authapp.models import ShopUser


class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email',
                    'is_superuser', 'is_active', 'avatar', 'age',)


admin.site.register(ShopUser, ShopUserAdmin)
