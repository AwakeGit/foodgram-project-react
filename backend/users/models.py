from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    """
    Модель подписки.
    Содержит информацию о том, кто на кого подписан.
    """

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='подписчики',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='авторы',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='подписчик-автор')
        ]

    def __str__(self):
        return f'{self.subscriber} подписан(а) на {self.author}'

    def clean(self):
        """
        Проверяет, что пользователь не может подписаться на самого себя.
        """
        if self.subscriber == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')
