from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from .validators import validate_hex_color

User = get_user_model()


class Tag(models.Model):
    """
    Модель для представления тегов в рецептах.
    """
    name = models.CharField(
        'Название.',
        max_length=30,
        help_text='Введите название.',
        db_index=True,
        unique=True
    )
    color = models.CharField(
        'Цвет в HEX.',
        max_length=7,
        null=True,
        validators=[validate_hex_color],
        help_text=(
            'Укажите цвет для тега в формате HEX.'
        ),
    )
    slug = models.SlugField(
        'Уникальный slug.',
        max_length=200,
        unique=True,
        help_text=(
            'Укажите уникальный slug для тега.'
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для представления ингредиентов в рецептах.
    """
    name = models.CharField(
        'Название.',
        max_length=200,
        db_index=True,
        help_text='Укажите название.',
    )
    measurement_unit = models.CharField(
        'Единицы измерения.',
        max_length=200,
        help_text=(
            'Укажите единицу измерения.'
        ),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для представления рецептов блюд.
    """
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта.',
    )
    name = models.CharField(
        'название',
        unique=True,
        max_length=200,
        help_text='Введите название блюда',
    )
    image = models.ImageField(
        'картинка блюда',
        upload_to='recipes/images/',
        help_text=(
            'Загрузите изображение блюда'
        ),
    )
    text = models.TextField(
        'описание',
        max_length=1000,
        help_text='Введите текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        help_text='Укажите теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления, мин',
        validators=(
            MinValueValidator(
                1,
                'Время приготовления должно быть больше нуля'),
            MaxValueValidator(
                180,
                'Время приготовления должно быть меньше 180 минут'),
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
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'id'),
                name='unique_recipes'
            ),
        )

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return self.name


class IngredientRecipe(models.Model):
    """
    Модель для представления связей между рецептами и ингредиентами.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
        help_text='Выберете ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_in_recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        help_text='Выберете рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(1200),
        ),
        help_text='Введите количество ингредиента в рецепте',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredient-recipe constraint')
        ]

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return self.recipe.name


class TagRecipe(models.Model):
    """
    Модель для представления связей между рецептами и тегами.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        help_text='Укажите рецепт',
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        help_text='Выберите тег',
        verbose_name='Тег',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тег рецептов'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return self.recipe.name


class Favorite(models.Model):
    """
    Модель для отслеживания избранных рецептов пользователями.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Укажите пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Выберите рецепт, добавляемый в избранное',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user-recipe constraint')
        ]

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return f'Пользователь {self.user} избрал рецепт {self.recipe}'


class ShoppingList(models.Model):
    """
    Модель для отслеживания списков покупок пользователей.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='пользователь',
        help_text=(
            'Укажите пользователя'
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
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user-recipe-shoppinglist constraint')
        ]

    def get_str_representation(self):
        """
        Возвращает строковое представление рецепта пользователя, добавленного в список покупок.
        """
        return f'{self.user} добавил рецепт "{self.recipe}" в список покупок'
