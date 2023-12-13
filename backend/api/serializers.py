from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite, Ingredient, IngredientRecipes,
    Recipe, ShoppingCart, Tag
)
from users.models import Subscription

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор."""

    class Meta:
        abstract = True
        fields = (
            'user',
            'recipe'
        )


class UserSerializer(UserSerializer):
    """Сериализатор пользователя."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Получает queryset с рецептами из избранного."""
        user = self.context.get('request').user
        return user.is_authenticated and Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения ингредиентов рецепта."""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipes
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи ингредиентов рецепта."""
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipes
        fields = (
            'id',
            'amount'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тега."""
    id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    image = Base64ImageField(read_only=True)
    ingredients = IngredientRecipeReadSerializer(
        many=True, source='amount_ingredients'
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        extra_kwargs = {
            'text': {'write_only': True},
        }

    def get_is_favorited(self, obj):
        """Получает queryset с рецептами из избранного."""
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Получает queryset с рецептами в корзине."""
        user = self.context.get('request').user
        return (
            user.is_authenticated and user.cart.filter(recipe=obj).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        self.validate_ingredients_presence(data)
        self.validate_tags_presence(data)
        self.validate_ingredient_weights(data)
        self.validate_unique_tags(data)

        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(
                {'cooking_time': 'Время готовки должно быть больше нуля'}

            )

        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными'
                )
            ingredients_list.append(ingredient['id'])

        return data

    def validate_ingredients_presence(self, data):
        """Проверяет наличие ингредиентов."""
        ingredients = data.get('ingredients', [])
        if not ingredients:
            raise serializers.ValidationError(
                'Необходимо добавить хотя бы один ингредиент')

    def validate_tags_presence(self, data):
        """Проверяет наличие тегов."""
        tags = data.get('tags', [])
        if not tags:
            raise serializers.ValidationError(
                'Необходимо добавить хотя бы один тег')

    def validate_ingredient_weights(self, data):
        """Проверяет вес ингредиента."""
        ingredients = data.get('ingredients', [])
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Вес ингредиента должен быть больше нуля')

    def validate_unique_tags(self, data):
        """Проверяет уникальность тегов."""
        tags = data.get('tags', [])
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги должны быть уникальными')

    def create_ingredients(self, ingredients, recipe):
        """Создаёт ингредиенты."""
        IngredientRecipes.objects.bulk_create(
            [IngredientRecipes(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Обновляет рецепт."""
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        super().update(instance, validated_data)
        self.create_ingredients(
            recipe=instance,
            ingredients=ingredients
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        """Получает queryset с рецептами из избранного."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор любимых рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteAndShoppingCartSerializerBase(BaseSerializer):
    """Сериализатор для добавления рецептов в избранное и корзину."""

    class Meta():
        model = Favorite
        fields = (
            'user',
            'recipe'
        )

    def validate(self, data):
        """Проверяет наличие рецепта в избранном."""
        user = data['user']
        recipe = data['recipe']
        model_class = self.Meta.model
        if model_class.objects.filter(user=user, recipe=recipe).exists():
            verbose_name_plural = model_class._meta.get_verbose_name_plural()
            raise serializers.ValidationError(
                f'Вы уже добавили рецепт в - {verbose_name_plural}'
            )
        return data


class FavoriteSerializer(FavoriteAndShoppingCartSerializerBase):
    """Сериализатор для рецептов из избранного."""

    class Meta(FavoriteAndShoppingCartSerializerBase.Meta):
        pass


class ShoppingCartSerializer(FavoriteAndShoppingCartSerializerBase):
    """Сериализатор для рецептов в корзине."""

    class Meta(FavoriteAndShoppingCartSerializerBase.Meta):
        model = ShoppingCart


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на рецепт."""

    class Meta:
        model = Subscription
        fields = (
            'user',
            'author'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
                message='Дважды на одного пользователя нельзя подписаться'
            )
        ]

    def validate(self, data):
        """Проверяет наличие рецепта в избранном."""
        if data['author'] == data['user']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data


class SubscriptionReadSerializer(UserSerializer):
    """Сериализатор чтения подписки на рецепт."""
    recipes = RecipeFavoriteSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        """Получает queryset с рецептами из избранного."""
        return obj.recipes.count()
