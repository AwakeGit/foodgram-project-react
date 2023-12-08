from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeFavoriteSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, ShoppingCartSerializer,
    SubscriptionReadSerializer, SubscriptionSerializer, TagSerializer,
    UserSerializer
)
from .utils import create_object, delete_object

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        """Получает набор запросов с рецептами."""
        return Recipe.objects.prefetch_related(
            'amount_ingredients__ingredient', 'tags'
        ).all()

    def perform_create(self, serializer):
        """Функция создания рецепта."""
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Получает сериализатор."""
        if self.action == 'retrieve' or self.action == 'list':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        """Получает queryset с рецептами из избранного."""
        if request.method == 'POST':
            serializer = create_object(
                request,
                pk,
                FavoriteSerializer,
                RecipeFavoriteSerializer,
                Recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete_object(request, pk, Recipe, Favorite)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        """Корзина покупок."""
        if request.method == 'POST':
            serializer = create_object(
                request,
                pk,
                ShoppingCartSerializer,
                RecipeFavoriteSerializer,
                Recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete_object(request, pk, Recipe, ShoppingCart)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачивание списка покупок."""
        ingredient_lst = ShoppingCart.objects.filter(
            user=request.user
        ).values_list(
            'recipe_id__ingredients__name',
            'recipe_id__ingredients__measurement_unit',
            Sum('recipe_id__ingredients__amount_ingredients__amount'))

        shopping_list = ['Список покупок:']
        ingredient_lst = set(ingredient_lst)

        for ingredient in ingredient_lst:
            shopping_list.append('{} ({}) - {}'.format(*ingredient))

        response = HttpResponse('\n'.join(shopping_list),
                                content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.txt"'
        )
        return response


class TagViewSet(viewsets.ModelViewSet):
    """Теги."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Ингредиенты."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        """Получает queryset с ингредиентами."""
        ingredients_name = self.request.query_params.get('name')
        if ingredients_name is not None:
            return Ingredient.objects.all().filter(
                name__istartswith=ingredients_name
            )
        return Ingredient.objects.all()


class CustomUserViewSet(UserViewSet):
    """Кастомный юзер."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id):
        """Подписка на авторов."""
        if request.method == 'POST':
            serializer = create_object(
                request,
                id,
                SubscriptionSerializer,
                SubscriptionReadSerializer,
                User
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        delete_object(request, id, User, Subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        """Подписки на авторов."""
        user = request.user
        authors = User.objects.filter(subscribing__user=user)

        paged_queryset = self.paginate_queryset(authors)
        serializer = SubscriptionReadSerializer(
            paged_queryset,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
