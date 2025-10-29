from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from products.models import Product, Category
from modules.services.utils import get_random_id, GetAdditionalData


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
        # basket = self.get_basket(request)
        # context["basket"] = basket
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
        # basket = self.get_basket(self.request.user)
        # context["basket"] = basket
        return context


class CategoryListView(ListView, GetAdditionalData):
    model = Product
    template_name = 'products/category_list.html'

    def get_queryset(self):
        cat_slug = self.kwargs["slug"]
        q_objects = Q()
        type_lst = self.request.GET.getlist("type")
        if type_lst:
            q_objects.add(Q(type__in=type_lst), Q.AND)
        material_lst = self.request.GET.getlist("material")
        if material_lst:
            q_objects.add(Q(material__in=material_lst), Q.AND)
        available_lst = self.request.GET.getlist("is_available")
        if available_lst:
            q_objects.add(Q(is_available__in=self.get_boolean(available_lst)), Q.AND)
        if q_objects:
            queryset = super().get_queryset().filter(q_objects,
                                                     category__slug=cat_slug)
        else:
            queryset = super().get_queryset().filter(category__slug=cat_slug)
        return queryset

    def get_ordering(self):
        ordering = self.request.GET.get("orderby")
        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs["slug"])
        context["title"] = "Категория -" + str(category)
        context["category"] = category
        context["category_types"] = self.get_types(category)
        context["category_materials"] = self.get_materials(category)
        context["available_num"] = self.get_available(category)
        context["not_available_num"] = self.get_not_available(category)
        # basket = self.get_basket(self.request.user)
        # context["basket"] = basket
        return context
