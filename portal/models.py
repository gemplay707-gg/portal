import secrets
from django.db import models
from django.contrib.auth.models import User

def generate_join_code():
    return secrets.token_urlsafe(6)[:6].upper()

# 1. Модель Навчального Класу
class SchoolClass(models.Model):
    ACCESS_CHOICES = [
        ('public', 'Публічний'),
        ('private', 'Приватний'),
    ]
    name = models.CharField(max_length=50, verbose_name="Назва класу (наприклад, 10-А)")
    access_type = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='public', verbose_name="Тип доступу")
    join_code = models.CharField(max_length=10, unique=True, default=generate_join_code, verbose_name="Код приєднання")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_classes', verbose_name="Вчитель/Творець")

    def __str__(self):
        return f"{self.name} ({self.get_access_type_display()})"

# 2. Модель Профілю Користувача (Повертаємо ForeignKey)
class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Учень'),
        ('teacher', 'Вчитель'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True, verbose_name="Нікнейм")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    avatar_url = models.URLField(blank=True, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png", verbose_name="Посилання на аватарку")
    
    # Повертаємо назад один клас
    school_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name="Клас")

    def __str__(self):
        return f"Профіль: {self.user.username}"

# 3. Модель повідомлень
class ClassMessage(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='messages', verbose_name="Клас")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Відправник")
    text = models.TextField(max_length=1000, verbose_name="Текст повідомлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата відправки")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.text[:20]}"