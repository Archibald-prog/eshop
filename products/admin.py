from django.contrib import admin
from products.models import (Category, ProductType,
                             Material, Product, ProductImages, ProductFeatures)

admin.site.register(ProductType)
admin.site.register(Material)
admin.site.register(ProductImages)
admin.site.register(ProductFeatures)
admin.site.site_header = 'Админ-панель интернет-магазина ESHOP'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", ]


class ProductTabAdmin(admin.TabularInline):
    model = ProductFeatures
    fields = "color", "dimensions", "detailed_desc"
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "material", "type",
                    "quantity", "price"]
    list_editable = ["quantity", "material", "price"]
    search_fields = ["name", "description", "category__name",
                     "type__name", "material__name"]
    list_filter = ["type", "material", "quantity", "category"]
    fields = [
        "name",
        "category",
        "type",
        "slug",
        "description",
        ("price", "old_price"),
        "quantity",
        "is_recommended",
        "is_new",
        "is_available",
        "is_hit",
        "is_active",
    ]

    inlines = [ProductTabAdmin]
