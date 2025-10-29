from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import auth
from authapp.forms import ShopUserRegisterForm, ShopUserLoginForm, ShopUserEditForm
from modules.services.utils import GetAdditionalData
from basketapp.models import Basket


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

    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('auth:logout'):
            return redirect_page
        return reverse_lazy('main')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                Basket.objects.filter(session_key=session_key).update(user=user)
                return HttpResponseRedirect(self.get_success_url())


class UserBasketView(TemplateView, GetAdditionalData):
    template_name = "authapp/user_basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "корзина"
        context["user_basket"] = True
        return context
