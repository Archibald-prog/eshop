import random
from pytils.translit import slugify
from products import models


def get_random_id(recommended=True):
    """
    Returns a list of IDs of products
    to be retrieved from the database
    """
    if recommended:
        initial_qs = models.Product.objects.filter(is_recommended=True)
    else:
        initial_qs = models.Product.objects.filter(is_new=True)
    random_list = random.sample(list(initial_qs), 8)
    random_id = [obj.id for obj in random_list]
    return random_id


def gen_slug(instance, slug):
    """Generates unique slugs for models"""
    model = instance.__class__
    unique_slug = slugify(slug)
    qs = model.objects.filter(slug=unique_slug).order_by('-id')
    while qs.exists():
        unique_slug = f'{unique_slug}-{qs.first().id}'
    return unique_slug


class GetAdditionalData:
    def get_link_menu(self):
        """
        Returns a collection of all product categories.
        """
        return models.Category.objects.all()

    def get_types(self, category):
        """
        Returns a collection of product types
        of a given category and the number of products of each type.
        """
        product_types = category.category_types.all()
        products_num = [prod_type.product_set.filter(
            category__slug=category.slug).count()
                        for prod_type in product_types]
        res_dict = {key: val for key, val in zip(product_types, products_num)}
        return res_dict

    def get_materials(self, category):
        """
        Returns a collection of materials associated
        with a given category and the number
        of products made of each material.
        """
        cat_products = models.Product.objects.filter(
            category__slug=category.slug).select_related("material")
        materials = [product.material for product in cat_products]
        materials_unique = list(dict.fromkeys(materials))
        products_num = [material.product_set.filter(
            category__slug=category.slug).count()
                        for material in materials_unique]
        res_dict = {key: val for key, val in zip(materials_unique, products_num)}
        return res_dict

    def get_available(self, category):
        """
        Returns a number of products
        of a given category available in stores.
        """
        return models.Product.objects.filter(category__slug=category.slug,
                                             is_available=True).count()

    def get_not_available(self, category):
        """
        Returns a number of products
        of a given category available only upon order.
        """
        return models.Product.objects.filter(category__slug=category.slug,
                                             is_available=False).count()

    def get_boolean(self, field_lst):
        raw_value = field_lst[0]
        if isinstance(raw_value, str):
            if raw_value.lower() == 'false':
                raw_value = False
            elif raw_value.lower() == 'true':
                raw_value = True
        return [raw_value]

    @staticmethod
    def get_user_basket(request):
        """
        Returns a collection of items
        in the current user's basket.
        """
        from basketapp import models
        if request.user.is_authenticated:
            return models.Basket.objects.filter(user=request.user).select_related('product')

        if not request.session.session_key:
            request.session.create()
        return models.Basket.objects.filter(session_key=request.session.session_key).select_related('product')
