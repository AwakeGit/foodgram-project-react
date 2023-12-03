from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token, TokenProxy
from rest_framework.authtoken.admin import TokenAdmin

from .models import Subscription

User = get_user_model()

admin.site.register(Subscription)


class CustomUserAdmin(UserAdmin):
    list_filter = ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.unregister(TokenProxy)


class MyTokenAdmin(TokenAdmin):
    pass


admin.site.register(Token, MyTokenAdmin)
