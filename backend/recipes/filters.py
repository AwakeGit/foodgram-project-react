from django_filters.rest_framework import FilterSet, filters

from .models import Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelMultipleChoiceFilter(
        field_name='author__id',
        to_field_name='id',
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'is_in_shopping_cart',
            'tags',
            'author',
        )

    def get_is_favorited(self, queryset, name, value):
        """Получает queryset с рецептами из избранного."""
        return queryset.filter(
            favorites__user=self.request.user) if value else queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Получает queryset с рецептами в корзине."""
        return queryset.filter(
            cart__user=self.request.user) if value else queryset
