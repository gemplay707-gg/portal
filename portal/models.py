from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Вибір ролей
    ROLE_CHOICES = [
        ('student', 'Учень'),
        ('teacher', 'Вчитель'),
        ('moderator', 'Модератор'),
        ('admin', 'Адміністратор'),
    ]

    # Зв'язок із вбудованим користувачем Django.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Наші кастомні поля
    nickname = models.CharField(max_length=50, blank=True, verbose_name="Нікнейм")
    user_class = models.CharField(max_length=10, blank=True, verbose_name="Клас (наприклад, 10-А)")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Про себе")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    
    # Посилання на дефолтну аватарку
    avatar_url = models.URLField(blank=True, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png", verbose_name="Посилання на аватарку")

    def __str__(self):
        return f"Профіль: {self.user.username}"