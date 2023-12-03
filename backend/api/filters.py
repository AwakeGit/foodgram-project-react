from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    """Набор фильтров для рецептов."""

    is_favorited = filters.BooleanFilter(method='filter_by_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_by_shopping_cart')
    author = filters.CharFilter(field_name='author__id')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    name = filters.CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'name']

    def filter_by_favorite(self, queryset, name, value):
        """Фильтрация по избранным рецептам."""
        user = self.request.user
        return queryset.filter(
            favorites__user=user) if (
                value and user.is_authenticated) else queryset

    def filter_by_shopping_cart(self, queryset, name, value):
        """Фильтрация по наличию в списке покупок."""
        user = self.request.user
        return queryset.filter(
            shoppinglist__user=user) if (
                value and user.is_authenticated) else queryset


class RecipeSearchFilter(SearchFilter):
    """Фильтр поиска для рецептов."""

    search_param = 'name'
