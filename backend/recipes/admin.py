from django.contrib import admin

from .forms import NotAllowEmptyForm
from .models import (
    Favorite, Ingredient, IngredientRecipes,
    Recipe, ShoppingCart, Tag
)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    # list_display = ('user_count')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class InlineBase(admin.TabularInline):
    """Интерфейс для создания связей между рецептами и ингредиентами."""
    extra = 0
    min_num = 1
    formset = NotAllowEmptyForm


class IngredientRecipeInline(InlineBase):
    """Интерфейс для создания связей между рецептами и ингредиентами."""
    model = IngredientRecipes


class TagInline(InlineBase):
    """Теги рецептов."""
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты."""
    list_display = ('id', 'name', 'author', 'pub_date', 'faivorites_count')
    list_filter = ('author', 'name', 'tags')
    exclude = ('tags',)
    inlines = [IngredientRecipeInline, TagInline]


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Корзина покупок."""
    list_display = ('user', 'recipe')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги."""
    list_display = ('name', 'color', 'slug')
