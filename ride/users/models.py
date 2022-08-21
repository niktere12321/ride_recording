from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    USER_ROLES = [
        (ADMIN, 'Admin role'),
        (USER, 'User role'),
    ]
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    active = models.BooleanField(default=True)
    phone_regex = RegexValidator(regex=r'^8\d{10}$', message="Нужно записать номер телефона в формате 89001112233.")
    phone = models.CharField(validators=[phone_regex], max_length=12, unique=True)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default='user',
    )

    class Meta:
        ordering = ('username',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
