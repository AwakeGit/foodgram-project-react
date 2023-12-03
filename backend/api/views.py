from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingList,
    Tag,
)
from recipes.permissions import AuthorOrReadOnly, ReadOnly
from users.models import Subscription

from .filters import IngredientFilter, RecipeFilter
from .serializers import (
    IngredientSerializer,
    MinimalRecipeSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    SpecialUserSerializer,
    TagSerializer,
    UserDetailSerializer,
)

User = get_user_model()


class SpecialUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = SpecialUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('email', 'username')
    pagination_class = PageNumberPagination

    @action(detail=False)
    def subscriptions(self, request):
        subscriber = self.request.user
        subscriptions = Subscription.objects.filter(subscriber=subscriber)
        authors = [subscription.author for subscription in subscriptions]

        page = self.paginate_queryset(authors)
        if page is not None:
            context = {'request': request}
            serializer = UserDetailSerializer(page, context=context, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserDetailSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    def subscription_actions(self, request, id=None):
        author = get_object_or_404(User, id=id)
        subscriber = self.request.user
        context = {'request': request}
        serializer = UserDetailSerializer(author, context=context)

        if subscriber == author:
            return Response({'error': 'Нельзя подписаться на самого себя'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            _, created = Subscription.objects.get_or_create(
                subscriber=subscriber,
                author=author
            )
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Подписка уже оформлена'},
                            status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscription.objects.filter(
            subscriber=subscriber,
            author=author
        ).first()

        if subscription:
            subscription.delete()
            return Response({'message': 'Подписка успешно удалена'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Подписка не найдена'},
                        status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('slug',)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'name', 'tags')
    filterset_class = RecipeFilter
    ordering = ('-pub_date',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = self.request.user
        objects_in_shopping_list = ShoppingList.objects.filter(user=user)
        lst = []
        for object in objects_in_shopping_list:
            id = object.recipe.id
            lst.append(id)
        instancies = IngredientRecipe.objects.filter(recipe_id__in=lst)
        my_dict = {}
        for instance in instancies:
            ingredient_id = instance.ingredient_id
            amount = instance.amount
            if ingredient_id not in my_dict:
                my_dict[ingredient_id] = amount
            else:
                my_dict[ingredient_id] += amount

        shopping_list = []

        for ingredient_id, amount in my_dict.items():
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient_name = ingredient.name
            ingredient_measurement_unit = ingredient.measurement_unit

            shopping_list.append(
                f'{ingredient_name} - {amount} {ingredient_measurement_unit}'
            )

        shopping_list_text = '\n'.join(shopping_list)

        my_file = f'Список покупок:\n{shopping_list_text}'
        response = HttpResponse(my_file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment'
        return response

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        context = {'request': request}
        serializer = MinimalRecipeSerializer(recipe, context=context)

        if request.method == 'POST':
            _, created = ShoppingList.objects.get_or_create(user=user,
                                                            recipe=recipe)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Рецепт уже в Списке покупок'},
                            status=status.HTTP_400_BAD_REQUEST)

        shoppinglist = ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        ).first()

        if shoppinglist:
            shoppinglist.delete()
            return Response(
                {'message': 'Рецепт успешно удален из Списка покупок'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response({'error': 'Рецепт не найден в Списке покупок'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        context = {'request': request}
        serializer = MinimalRecipeSerializer(recipe, context=context)

        if request.method == 'POST':
            _, created = Favorite.objects.get_or_create(user=user,
                                                        recipe=recipe)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'error': 'Рецепт уже в Избранном'},
                            status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).first()

        if favorite:
            favorite.delete()
            return Response(
                {'message': 'Рецепт успешно удален из Избранного'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response({'error': 'Рецепт не найден в Избранном'},
                        status=status.HTTP_400_BAD_REQUEST)
