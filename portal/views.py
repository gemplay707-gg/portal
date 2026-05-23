from django.shortcuts import render
from django.views.generic import TemplateView

# Створюємо представлення для головної сторінки
class HomePageView(TemplateView):
    template_name = 'portal/home.html'