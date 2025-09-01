import random
from django.views.generic import ListView, DetailView
from products.models import Product


def get_random_id(recommended=True):
    if recommended:
        initial_qs = Product.objects.filter(is_recommended=True)
    else:
        initial_qs = Product.objects.filter(is_new=True)
    random_list = random.sample(list(initial_qs), 8)
    random_id = [obj.id for obj in random_list]
    return random_id


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        id_list = get_random_id()
        return Product.objects.filter(pk__in=id_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "товары/главная"
        id_list = get_random_id(recommended=False)
        new_products = Product.objects.filter(pk__in=id_list)
        context["new_products"] = new_products
        return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "товары/товар"
        obj = context["object"]
        features = obj.productfeatures_set.all().first()
        same_products = Product.objects.filter(category=obj.category).exclude(pk=obj.pk)
        context["same_products"] = same_products
        context["features"] = features
        return context
