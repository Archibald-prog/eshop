from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.shortcuts import resolve_url
from django.conf import settings
from authapp.forms import ShopUserRegisterForm, ShopUserLoginForm, ShopUserEditForm
from modules.services.utils import GetAdditionalData
from basketapp.models import Basket
from orders.models import Order, OrderItem


class RegisterShopUser(CreateView, GetAdditionalData):
    form_class = ShopUserRegisterForm
    template_name = "authapp/register.html"
    success_url = reverse_lazy("auth:login")
    extra_context = {"title": "Регистрация",
                     "register": True}


class EditShopUser(UpdateView, GetAdditionalData):
    form_class = ShopUserEditForm
    template_name = "authapp/edit.html"
    success_url = reverse_lazy("auth:user_profile")
    extra_context = {"title": "Редактирование профиля",
                     "edit": True}

    def get_object(self, *args, **kwargs):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Аккаунт успешно обновлен")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)


class LoginShopUser(LoginView, GetAdditionalData):
    form_class = ShopUserLoginForm
    template_name = "authapp/login.html"
    extra_context = {"title": "Вход", "login": True}

    def get_default_redirect_url(self):
        if 'orders' in self.request.META.get('HTTP_REFERER'):
            self.next_page = reverse('orders:create_order')
            return resolve_url(self.next_page)
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                Basket.objects.filter(session_key=session_key).update(user=user)
                messages.success(self.request, f"{user.first_name}, вы вошли в аккаунт")
                return HttpResponseRedirect(self.get_default_redirect_url())


class UserBasketView(TemplateView, GetAdditionalData):
    template_name = "authapp/user_basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "корзина"
        context["user_basket"] = True
        return context


class UserProfileView(ListView, GetAdditionalData):
    template_name = "authapp/user_profile.html"
    context_object_name = 'orders'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "профиль пользователя"
        context["user_profile"] = True
        return context
