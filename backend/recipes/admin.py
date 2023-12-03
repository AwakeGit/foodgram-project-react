from django.contrib import admin

from .forms import InlineFormSet
from .models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingList,
    Tag,
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    formset = InlineFormSet


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingList)
admin.site.register(IngredientRecipe)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline, )
    list_filter = ('author', 'name', 'tags')
    list_display = ('name', 'author', 'number_of_additions_to_favorites')

    def number_of_additions_to_favorites(self, obj):
        return obj.favorited_by.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name', 'measurement_unit')
