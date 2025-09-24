from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from authapp.forms import ShopUserRegisterForm, ShopUserLoginForm, ShopUserEditForm
from modules.services.utils import GetAdditionalData


class RegisterShopUser(CreateView, GetAdditionalData):
    form_class = ShopUserRegisterForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy("auth:login")
    extra_context = {"title": "Регистрация",
                     "register": True}


class EditShopUser(UpdateView, GetAdditionalData):
    form_class = ShopUserEditForm
    template_name = "authapp/edit.html"
    success_url = reverse_lazy("main")
    extra_context = {"title": "Редактирование профиля",
                     "edit": True}

    def get_object(self, *args, **kwargs):
        return self.request.user


class LoginShopUser(LoginView, GetAdditionalData):
    form_class = ShopUserLoginForm
    template_name = "authapp/login.html"
    extra_context = {"title": "Вход", "login": True}

