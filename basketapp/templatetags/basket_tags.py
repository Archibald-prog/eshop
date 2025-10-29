from django import template
from modules.services.utils import GetAdditionalData

register = template.Library()


@register.simple_tag()
def user_baskets(request):
    return GetAdditionalData.get_user_basket(request)
