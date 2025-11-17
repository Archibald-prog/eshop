from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from modules.services.utils import GetAdditionalData
from basketapp.models import Basket
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView, GetAdditionalData):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy('main')
    success_message = None

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                basket_items = Basket.objects.filter(user=user)

                if basket_items.exists():
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    for basket_item in basket_items:
                        product = basket_item.product
                        name = basket_item.product.name
                        price = basket_item.product.price
                        quantity = basket_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточо товара {name} на складе. '
                                                  f'В наличии - {product.quantity}.')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        if product.quantity < 1:
                            product.is_available = False
                            product.is_active = False
                        product.save()

                    basket_items.delete()
                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect('main')
        except ValidationError as e:
            messages.warning(self.request, *e)
            return redirect('orders:create_order')

    def form_invalid(self, form):
        messages.warning(self.request,
                         'Заполните все обязательные поля!')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        context["orders"] = True
        return context
