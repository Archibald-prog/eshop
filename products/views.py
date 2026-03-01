from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from products.models import Product, Category
from modules.services.utils import get_random_id, GetAdditionalData


class ProductListView(ListView, GetAdditionalData):
    model = Product

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = Product.objects.filter(Q(name__iregex=search_query) |
                                              Q(category__name__iregex=search_query) |
                                              Q(type__name__iregex=search_query) |
                                              Q(material__name__iregex=search_query) |
                                              Q(description__iregex=search_query))
        else:
            id_list = get_random_id()
            queryset = Product.objects.filter(pk__in=id_list)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "товары/главная"
        id_list = get_random_id(recommended=False)
        new_products = Product.objects.filter(pk__in=id_list)
        context["new_products"] = new_products
        if 'search' in self.request.GET:
            context['searching'] = True
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
    paginate_by = 6

    def get_queryset(self):
        cat_slug = self.kwargs["slug"]
        queryset = (Product.objects.filter(category__slug=cat_slug).
                    select_related('category', 'type', 'material'))

        q_objects = Q()
        type_lst = self.request.GET.getlist("type")
        if type_lst:
            q_objects &= Q(type__id__in=type_lst)

        material_lst = self.request.GET.getlist("material")
        if material_lst:
            q_objects &= Q(material__id__in=material_lst)

        available_lst = self.request.GET.getlist("is_available")
        if available_lst:
            # Преобразуем ['True'] или ['False'] в булевы значения
            bool_vals = [val.lower() == 'true' for val in available_lst]
            q_objects &= Q(is_available__in=bool_vals)

        queryset = queryset.filter(q_objects)

        # Сортировка (всегда добавляем 'id' вторым для стабильной пагинации)
        ordering = self.request.GET.get("orderby")
        if ordering:
            queryset = queryset.order_by(ordering, "id")
        else:
            queryset = queryset.order_by("id")

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Подготовка параметров для ссылок пагинации
        params = self.request.GET.copy()
        params.pop('page', None)
        context['url_params'] = params.urlencode()

        # Списки для сохранения галочек в чекбоксах
        context["selected_types"] = self.request.GET.getlist("type")
        context["selected_materials"] = self.request.GET.getlist("material")
        context["selected_availability"] = self.request.GET.getlist(
            "is_available")

        category = get_object_or_404(Category, slug=self.kwargs["slug"])
        context.update({
            "title": f"Категория - {category}",
            "category": category,
            "category_types": self.get_types(category),
            "category_materials": self.get_materials(category),
            "available_num": self.get_available(category),
            "not_available_num": self.get_not_available(category),
        })
        return context
