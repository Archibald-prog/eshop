from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic.base import View
from basketapp.models import Basket
from products.models import Product
from basketapp.mixins import CartMixin


class BasketAdd(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        basket = self.get_basket_product(request, product=product)

        if basket:
            basket.quantity += 1
            basket.save()
        else:
            Basket.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key
                if not request.user.is_authenticated else None,
                product=product, quantity=1)

        response_data = {
            "message": "Товар добавлен в корзину",
            'cart_items_html': self.render_basket(request)
        }
        return JsonResponse(response_data)


class BasketRemove(CartMixin, View):
    def post(self, request):
        basket_id = request.POST.get("cart_id")
        basket_record = get_object_or_404(Basket, pk=basket_id)
        quantity = basket_record.quantity
        basket_record.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            "cart_items_html": self.render_basket(request)
        }
        return JsonResponse(response_data)


class BasketEdit(CartMixin, View):
    def post(self, request):
        basket_id = request.POST.get("cart_id")
        basket_item = Basket.objects.get(pk=int(basket_id))

        fields = {
            "quantity": int(request.POST.get("quantity")),
        }

        updated = False
        for field, value in fields.items():
            if value is not None:
                setattr(basket_item, field, value)
                updated = True

        if updated:
            basket_item.save()

        return JsonResponse(self._get_basket_response(request))

    def _get_basket_response(self, request):
        """Helper method for generating a JSON response from the cart"""

        total_quantity = Basket.objects.filter(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key
            if not request.user.is_authenticated else None
        ).total_quantity()

        return {
            "message": "Количество товара изменено",
            "total_quantity": total_quantity,
            "cart_items_html": self.render_basket(request),
        }
