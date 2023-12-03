from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token

from .models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Subscription.
    Отображает подписчиков и авторов подписок.
    """
    list_filter = ('subscriber', 'author')

    def __str__(self, obj):
        """
        Возвращает строковое представление подписки.
        """
        return f'{obj.subscriber} подписан(а) на {obj.author}'


class CustomUserAdmin(UserAdmin):
    """
    Пользовательский административный интерфейс для модели User.
    Отображает имена пользователей и их электронные адреса.
    """
    list_filter = ('username', 'email')


class MyTokenAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Token.
    """
    pass


# Регистрация моделей с пользовательскими классами администратора
User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Token, MyTokenAdmin)
