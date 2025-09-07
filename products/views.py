import random
from django.views.generic import ListView, DetailView
from products.models import Product, Category


def get_random_id(recommended=True):
    if recommended:
        initial_qs = Product.objects.filter(is_recommended=True)
    else:
        initial_qs = Product.objects.filter(is_new=True)
    random_list = random.sample(list(initial_qs), 8)
    random_id = [obj.id for obj in random_list]
    return random_id

class GetAdditionalData:
    def get_link_menu(self):
        return Category.objects.all()


class ProductListView(ListView, GetAdditionalData):
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


class ProductDetailView(DetailView, GetAdditionalData):
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


class CategoryListView(ListView, GetAdditionalData):
    model = Product
    template_name = 'products/category_list.html'

    def get_queryset(self):
        cat_slug = self.kwargs['slug']
        queryset = Product.objects.filter(category__slug=cat_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["object_list"][0].category
        context["title"] = "Категория -" + str(category)
        context["category"] = category
        return context
