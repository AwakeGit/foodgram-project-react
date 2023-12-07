from django.contrib import admin
from recipes.forms import NotAllowEmptyForm
from recipes.models import (
    Favorite, Ingredient,
    IngredientRecipes, Recipe,
    ShoppingCart, Tag
)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Листинг избранных рецептов."""
    list_display = ('user', 'recipe')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ингредиенты."""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class InlineBase(admin.TabularInline):
    """Инлайн для рецептов."""
    extra = 0
    min_num = 1
    formset = NotAllowEmptyForm


class IngredientRecipeInline(InlineBase):
    """Ингредиенты рецепта."""
    model = IngredientRecipes


class TagInline(InlineBase):
    """Теги рецепта."""
    model = Recipe.tags.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты."""
    list_display = ('id', 'name', 'author', 'pub_date')
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
