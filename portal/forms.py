from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    # Додаємо унікальне системне ім'я та email
    username = forms.CharField(label="Нікнейм на порталі", required=True)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    # Перевірка, чи не зайнятий новий нікнейм кимось іншим
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Цей нікнейм уже зайнятий іншим користувачем!")
        return username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Прибираємо звідси 'nickname', залишаємо тільки інші поля
        fields = ['user_class', 'bio', 'avatar_url']