from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        verbose_name='Email адрес',
        unique=True,
        max_length=254,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        null=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def subscription_count(self):
        return self.subscribing.count()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.first_name


class Subscription(models.Model):
    """Класс подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_subscriber'
        )]

    def __str__(self):
        """Возвращает строковое представление подписки."""
        return f'{self.user} подписан на {self.author}'
