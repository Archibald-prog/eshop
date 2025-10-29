from django.urls import path
from django.contrib.auth.views import LogoutView

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.LoginShopUser.as_view(),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='auth:login'),
         name='logout'),
    path('register/', authapp.RegisterShopUser.as_view(),
         name='register'),
    path('edit/', authapp.EditShopUser.as_view(),
         name='edit'),
    path('user-basket/', authapp.UserBasketView.as_view(),
         name='user_basket'),
]
