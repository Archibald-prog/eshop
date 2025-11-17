"""
URL configuration for eshop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("products.urls")),
    path('auth/', include("authapp.urls", namespace="auth")),
    path('basket/', include("basketapp.urls", namespace="basket")),
    path('orders/', include("orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
