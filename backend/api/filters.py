from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    BooleanFilter,
    CharFilter,
    ModelMultipleChoiceFilter,
)

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):

    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_list'
    )
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all(),)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            favorite_instancies = user.favorites.all()
            favorite_recipes_id = []
            for favorite_instance in favorite_instancies:
                favorite_recipes_id.append(favorite_instance.recipe.id)
            return queryset.filter(id__in=favorite_recipes_id)
        return queryset

    def filter_is_in_shopping_list(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            shoppinglist_instancies = user.shopping_lists.all()
            shoppinglist_recipes_id = []
            for shoppinglist_instance in shoppinglist_instancies:
                shoppinglist_recipes_id.append(shoppinglist_instance.recipe.id)
            return queryset.filter(id__in=shoppinglist_recipes_id)
        return queryset
