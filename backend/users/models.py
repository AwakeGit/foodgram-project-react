from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
# from rest_framework.authtoken.models import Token

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='подписчик',
        help_text=(
            'Выберете пользователя, который подписывается '
            'на того или иного автора рецептов'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='автор рецепта',
        help_text=(
            'Выберете автора рецептов, на которого подписывается тот или иной '
            '(выбранный ранее) пользователь'
        ),
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'author'],
                                    name='subscriber-author constraint')
        ]

    def __str__(self):
        return f'{self.subscriber} подписан(а) на {self.author}'

    def clean(self):
        if self.subscriber == self.author:
            raise ValidationError('Нельзя подписаться на самого себя')


# class CustomToken(Token):

#     class Meta:
#         verbose_name = 'Токен'
#         verbose_name_plural = 'Токены'
