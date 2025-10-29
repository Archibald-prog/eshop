from django.template.loader import render_to_string
from modules.services.utils import GetAdditionalData
from basketapp.models import Basket


class CartMixin(GetAdditionalData):
    def get_basket_product(self, request, product=None, cart_id=None):
        """
        Returns a Basket model object
        associated with a given product
        and the current user.
        """
        query_kwargs = {}
        if request.user.is_authenticated:
            query_kwargs["user"] = request.user
        if product:
            query_kwargs["product"] = product
        if cart_id:
            query_kwargs["id"] = cart_id
        return Basket.objects.filter(**query_kwargs).first()

    def render_basket(self, request):
        """
        Returns an updated version
        of the basket html markup.
        """
        user_cart = self.get_user_basket(request)
        context = {"carts": user_cart}

        return render_to_string(
            "basketapp/includes/inc_basket_list.html",
            context, request=request)
