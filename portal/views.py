from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile

# 1. Головна сторінка
class HomePageView(TemplateView):
    template_name = 'portal/home.html'

# 2. Сторінка реєстрації
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# 3. Сторінка профілю (доступна тільки авторизованим користувачам)
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'portal/profile.html'
    context_object_name = 'profile'

    # Автоматично підтягуємо профіль того, хто зараз увійшов на сайт
    def get_object(self, queryset=None):
        return self.request.user.profile