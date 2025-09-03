from django.urls import path

from products import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(),
         name="product_detail"),
]
