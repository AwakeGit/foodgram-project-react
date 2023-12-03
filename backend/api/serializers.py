import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (
    ImageField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
    ValidationError,
)

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingList,
    Tag,
)
from users.models import Subscription

User = get_user_model()


class SpecialUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        subscriber = self.context['request'].user
        return subscriber.is_authenticated and Subscription.objects.filter(
            subscriber=subscriber, author=obj
        ).exists() or False


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)

        return super().to_internal_value(data)


class MinimalRecipeSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserDetailSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()
    recipes = MinimalRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(author=obj).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SpecialUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    author = SpecialUserSerializer()
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='ingredients_in_recipe')
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
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
        ]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Favorite.objects.filter(
            user=user, recipe=obj
        ).exists() or False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and ShoppingList.objects.filter(
            user=user, recipe=obj
        ).exists() or False


class IngredientRecipeCreateSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = SpecialUserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
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
        ]

    def validate_ingredients(self, ingredients):
        existing_ingredients = []

        if not ingredients:
            raise ValidationError(
                [{'name': ['Укажите хотя бы один ингредиент']}]
            )

        for ingredient in ingredients:
            if ingredient['id'] in existing_ingredients:
                raise ValidationError(
                    [{'name': ['Ингредиенты не должны повторяться']}]
                )
            existing_ingredients.append(ingredient['id'])

        return ingredients

    def validate_tags(self, tags):
        existing_tags = []

        if not tags:
            raise ValidationError('Укажите хотя бы один тэг')

        for tag in tags:
            if tag in existing_tags:
                raise ValidationError('Тэги не должны повторяться')
            existing_tags.append(tag)

        return tags

    def validate_cooking_time(self, cooking_time):
        if not isinstance(cooking_time, int) or cooking_time < 1:
            raise ValidationError(
                'Время готовки должно быть целым положительным числом'
            )
        return cooking_time

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            IngredientRecipe(
                ingredient=ingredient_data['id'],
                recipe=recipe,
                amount=ingredient_data['amount']
            ).save()

        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        ingredients = instance.ingredients

        instance.tags.set(validated_data.get('tags', instance.tags.all()))
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        ingredients.clear()

        for ingredient_data in ingredients_data:
            IngredientRecipe(
                ingredient=ingredient_data['id'],
                recipe=instance,
                amount=ingredient_data['amount']
            ).save()

        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Favorite.objects.filter(
            user=user, recipe=obj
        ).exists() or False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and ShoppingList.objects.filter(
            user=user, recipe=obj
        ).exists() or False

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data
