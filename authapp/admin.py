from django.contrib import admin
from authapp.models import ShopUser
from basketapp.admin import BasketTabAdmin
from orders.admin import OrderTabAdmin


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email',
                    'is_superuser', 'is_active', 'age', ]
    search_fields = ['username', 'first_name', 'last_name', 'email', ]
    list_filter = ['is_superuser', 'is_active', 'age',]
    inlines = [BasketTabAdmin, OrderTabAdmin]
