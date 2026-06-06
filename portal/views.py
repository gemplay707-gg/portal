from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

# Головна сторінка
class HomePageView(TemplateView):
    template_name = 'portal/home.html'

# Реєстрація
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Перегляд профілю
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'portal/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

# Редагування профілю (функція)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'portal/edit_profile.html', context)