from django import forms
from django.contrib.auth.models import User
from .models import Profile, SchoolClass

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Нікнейм на порталі", required=True)
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Цей нікнейм уже зайнятий іншим користувачем!")
        return username

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school_class', 'bio', 'avatar_url']

class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name', 'access_type']
        labels = {
            'name': 'Назва класу (наприклад, 10-А)',
            'access_type': 'Тип доступу',
        }

class ClassJoinForm(forms.Form):
    join_code = forms.CharField(
        max_length=10, 
        label="Введіть 6-значний код приєднання",
        widget=forms.TextInput(attrs={'placeholder': 'Наприклад, X4Y7ZW'})
    )

    def clean_join_code(self):
        code = self.cleaned_data.get('join_code').upper().strip()
        if not SchoolClass.objects.filter(join_code=code).exists():
            raise forms.ValidationError("Клас із таким кодом не знайдено!")
        return code