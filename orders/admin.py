from django.contrib import admin
from orders.models import Order, OrderItem


class OrderTabAdmin(admin.TabularInline):
    model = Order
    fields = ("phone_number", "status", "payment_on_get",
              "created_timestamp", "is_paid",)
    readonly_fields = ("created_timestamp",)
    extra = 1


class OrderItemTabAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("name", "price", "quantity",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "phone_number",
                    "requires_delivery", "is_paid", "payment_on_get",
                    "status", "created_timestamp", ]
    list_filter = ["id", "user", "phone_number", "created_timestamp", ]
    list_display_links = ["id", ]
    search_fields = ["user__name", "phone_number"]
    inlines = [OrderItemTabAdmin]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "name", "price",
                    "quantity", "created_timestamp",]
    list_filter = ["order", "quantity", "created_timestamp",]
    search_fields = ["name", "created_timestamp",]
