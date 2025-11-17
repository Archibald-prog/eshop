from django.urls import path
import orders.views as orders

app_name = 'orders'

urlpatterns = [
    path('create-order/', orders.CreateOrderView.as_view(),
         name="create_order"),
]
