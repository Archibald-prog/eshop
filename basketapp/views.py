from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
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
            "quantity_deleted": quantity,
            "cart_items_html": self.render_basket(request)
        }
        return JsonResponse(response_data)


class BasketEdit(CartMixin, View):
    def post(self, request):
        basket_id = request.POST.get("cart_id")
        basket_item = Basket.objects.get(pk=int(basket_id))
        item_quantity = int(request.POST.get("quantity"))

        if item_quantity > 0:
            basket_item.quantity = item_quantity
            basket_item.save()
        else:
            basket_item.delete()

        total_quantity = Basket.objects.filter(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key
            if not request.user.is_authenticated else None
        ).total_quantity()

        response_data = {
            "quantity": item_quantity,
            "total_quantity": total_quantity,
            "cart_items_html": self.render_basket(request),
        }
        return JsonResponse(response_data)
