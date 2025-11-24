from django.contrib import admin
from basketapp.models import Basket



class BasketTabAdmin(admin.TabularInline):
    model = Basket
    fields = ("product", "quantity", "add_datetime",)
    readonly_fields = ("add_datetime",)
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product", "quantity", "add_datetime", ]
    list_filter = ["add_datetime", "user", "product__name", ]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
