from django.contrib import admin
from .models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingList,
    Tag,
    TagRecipe,
    Favorite
)


class TagRecipeInline(admin.TabularInline):
    """
    Встраиваемый класс для отображения связанных моделей
    TagRecipe в административном интерфейсе Recipe.
    """
    model = TagRecipe
    extra = 1


class IngredientRecipeInline(admin.TabularInline):
    """
    Встраиваемый класс для отображения связанных моделей
    IngredientRecipe в административном интерфейсе Recipe.
    """
    model = IngredientRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели Recipe.
    """
    readonly_fields = ('get_number_of_favorites',)
    list_display = ('name', 'author')
    search_fields = ('author__username', 'author__email', 'name')
    inlines = [IngredientRecipeInline, TagRecipeInline]
    list_filter = ('tags',)
    empty_value_display = '-empty-'

    def get_number_of_favorites(self, obj):
        """
        Метод для получения количества добавлений в избранное для
        конкретного рецепта.
        """
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели Ingredient.
    """
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-empty-'
    inlines = [IngredientRecipeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели Tag.
    """
    list_display = ('id', 'name', 'color')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
    inlines = [TagRecipeInline, ]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели Favorite.
    """
    list_display = ('id', 'recipe', 'user')
    search_fields = ('recipe__name', 'user__username', 'user__email')
    list_filter = ('recipe__tags__name',)
    empty_value_display = '-empty-'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели ShoppingList.
    """
    list_display = ('id', 'recipe', 'user')
    search_fields = ('recipe__name', 'user__username', 'user__email')
    empty_value_display = '-empty-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели IngredientRecipe.
    """
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    """
    Класс настройки административного интерфейса для модели TagRecipe.
    """
    search_fields = ('tag__name', 'recipe__name')
    list_filter = ('tag',)
