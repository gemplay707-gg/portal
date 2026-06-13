from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Profile, SchoolClass, ClassMessage
from .forms import UserUpdateForm, ProfileUpdateForm, ClassCreateForm, ClassJoinForm

# Головна сторінка
def home_page(request):
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        current_class = profile.school_class
    else:
        current_class = None

    return render(request, 'portal/home.html', {'current_class': current_class})

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

# Редагування профілю
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'portal/edit_profile.html', context)


# ================= ЛОГІКА КЛАСІВ =================

@login_required
def classes_dashboard(request):
    public_classes = SchoolClass.objects.filter(access_type='public')
    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'public_classes': public_classes,
        'my_profile': profile,
        'create_form': ClassCreateForm(),
        'join_form': ClassJoinForm(),
    }
    return render(request, 'portal/classes.html', context)

@login_required
def create_class(request):
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.teacher = request.user
            new_class.save()
            
            # Прив'язуємо створений клас до профілю
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.school_class = new_class
            profile.save()
            
            messages.success(request, f"Клас '{new_class.name}' успішно створено! Код: {new_class.join_code}")
    return redirect('classes_dashboard')

@login_required
def join_class(request, class_id=None):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Публічний клас
    if class_id:
        target_class = get_object_or_404(SchoolClass, id=class_id, access_type='public')
        profile.school_class = target_class
        profile.save()
        messages.success(request, f"Ви успішно вступили до класу: {target_class.name}")
        return redirect('classes_dashboard')

    # Приватний за кодом
    if request.method == 'POST':
        form = ClassJoinForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('join_code').upper().strip()
            target_class = SchoolClass.objects.get(join_code=code)
            profile.school_class = target_class
            profile.save()
            messages.success(request, f"Ви успішно приєдналися до класу: {target_class.name}")
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
                
    return redirect('classes_dashboard')

@login_required
def class_room(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Перевірка: користувач або учень цього класу, або його творець
    if profile.school_class != school_class and school_class.teacher != request.user:
        messages.error(request, "Ви не маєте доступу до цього класу!")
        return redirect('home')

    if request.method == 'POST':
        message_text = request.POST.get('message_text', '').strip()
        if message_text:
            ClassMessage.objects.create(
                school_class=school_class,
                sender=request.user,
                text=message_text
            )
            return redirect('class_room', class_id=school_class.id)

    return render(request, 'portal/class_room.html', {
        'school_class': school_class,
        'chat_messages': school_class.messages.all(),
        'students': school_class.students.all(),
    })