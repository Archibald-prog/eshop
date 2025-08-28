from django.contrib import admin
from products.models import (Category, ProductType,
                             Material, Product, ProductImages, ProductFeatures)

admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Material)
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(ProductFeatures)
