from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    SpecialUserViewSet,
    TagViewSet,
)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('users', SpecialUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
