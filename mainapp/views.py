from django.views.generic import ListView, TemplateView
from mainapp.models import Contact
from modules.services.utils import GetAdditionalData


class ConactListView(ListView, GetAdditionalData):
    model = Contact
    template_name = 'mainapp/contact_list.html'
    extra_context = {"title": "Контакты", "contact": True}


class SupplyView(TemplateView, GetAdditionalData):
    template_name = 'mainapp/supply.html'
    extra_context = {"title": "Поставщикам", "supply": True}
