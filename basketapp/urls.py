from django.urls import path
import basketapp.views as basketapp

app_name = "basketapp"

urlpatterns = [
    path('add/', basketapp.BasketAdd.as_view(), name="add"),
    path('remove/', basketapp.BasketRemove.as_view(), name="remove"),
    path('edit/', basketapp.BasketEdit.as_view(), name="edit"),
]