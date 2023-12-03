import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


def validate_hex_color(value):
    hex_color_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    if not re.match(hex_color_pattern, value):
        raise ValidationError(
            'Введите цвет в формате HEX (например, "#E26C2D").'
        )


class Tag(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        unique=True,
        help_text='Введите название нового тега (не более 200 символов)',
    )
    color = models.CharField(
        'цвет в HEX',
        max_length=7,
        unique=True,
        validators=[validate_hex_color],
        help_text=(
            'Укажите цвет для тега в формате HEX '
            '(не более 7 символов, включая знак "#"). Например "#E26C2D"'
        ),
    )
    slug = models.SlugField(
        'уникальный слаг',
        max_length=200,
        unique=True,
        help_text=(
            'Введите уникальный слаг - строку, максимальной длиной '
            'не более 200 символов, состоящую из букв, цифр, дефиса и '
            'знака подчёркивания'
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:50] if len(self.name) > 50 else self.name

    def clean(self):
        self.color = self.color.upper()


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=200,
        help_text=(
            'Введите название нового ингредиента (не более 200 символов)'
        ),
    )
    measurement_unit = models.CharField(
        'единицы измерения',
        max_length=200,
        help_text=(
            'Введите подходящие единицы измерения для нового ингредиента'
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:50] if len(self.name) > 50 else self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='автор рецепта',
        help_text='Выберете автора рецепта из предложенного перечня',
    )
    name = models.CharField(
        'название',
        unique=True,
        max_length=200,
        help_text='Введите название блюда (название рецепта)',
    )
    image = models.ImageField(
        'картинка блюда',
        upload_to='recipes/images/',
        help_text=(
            'Укажите ссылку на картинку в Base64: '
            'Например: data:image/png;base64,iVBORw0KGgo...'
        ),
    )
    text = models.TextField(
        'описание',
        help_text='Введите текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='список ингредиентов',
        help_text='Выберете ингредиенты в требуемом количестве.',
        through='IngredientRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='список тегов',
        help_text='Выберете нужные теги.',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления (в минутах)',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(32767),
        ),
        help_text='Укажите время приготовления блюда',
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:50] if len(self.name) > 50 else self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='Выберете ингредиент из предложенного перечня',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберете рецепт из предложенного перечня!',
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(32767),
        ),
        help_text='Задайте требуемое количество для выбранного ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='ingredient-recipe constraint')
        ]

    def __str__(self):
        return (
            f'{self.recipe}: {self.ingredient}, '
            f'{self.amount} {self.ingredient.measurement_unit}'
        )


class BaseModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name=None,
        verbose_name=None,
        help_text=None,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name=None,
        verbose_name=None,
        help_text=None,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_str_representation()


class Favorite(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
        help_text=(
            'Выберете пользователя, который добавляет тот или иной рецепт '
            'в избранное'
        ),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='рецепт',
        help_text='Выберете рецепт, добавляемый в избранное',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='user-recipe constraint')
        ]

    def get_str_representation(self):
        return f'{self.user} добавил(а) рецепт "{self.recipe}" в избранное'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='пользователь',
        help_text=(
            'Выберете пользователя, который добавляет тот или иной рецепт '
            'в список покупок'
        ),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='рецепт',
        help_text='Выберете рецепт, добавляемый в список покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='user-recipe-shoppinglist constraint')
        ]

    def get_str_representation(self):
        return (
            f'{self.user} добавил(а) рецепт "{self.recipe}" '
            f'в список покупок'
        )
