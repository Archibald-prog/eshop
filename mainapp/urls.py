from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('contact/', mainapp.ConactListView.as_view(), name="contact"),
    path('supply/', mainapp.SupplyView.as_view(), name="supply"),
]