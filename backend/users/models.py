from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        help_text='Логин'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        help_text='Пароль'
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        help_text='Электронная почта'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        help_text='Имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        help_text='Фамилия'
    )

    role = models.CharField(
        'Роль',
        max_length=15,
        blank=False,
        help_text='Роль пользователя',
        choices=[('user', 'Пользователь'),
                 ('admin', 'Администратор')],
        default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.groups.filter(name='admin').exists()

    def __str__(self):
        return self.username
