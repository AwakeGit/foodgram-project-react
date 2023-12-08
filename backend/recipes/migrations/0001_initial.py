# Generated by Django 3.2 on 2023-12-06 22:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=200,
                                          verbose_name='Название ингридиента')),
                ('measurement_unit', models.CharField(max_length=200,
                                                      verbose_name='Еденицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[
                    django.core.validators.MinValueValidator(1,
                                                             'Количество должно быть равно хотя бы одному')],
                                                            verbose_name='Количество')),
                ('ingredient',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='amount_ingredients',
                                   to='recipes.ingredient',
                                   verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингредиенты рецепта',
                'ordering': ['recipe'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=200,
                                          verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipes/images',
                                            verbose_name='Изображение')),
                ('text',
                 models.TextField(max_length=1000, verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(validators=[
                    django.core.validators.MinValueValidator(1,
                                                             'Время приготовления должно бытьравно хотя бы одной минуте')],
                                                                  verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True,
                                                  verbose_name='Дата и время публикации рецепта')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='recipes',
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes',
                                                       through='recipes.IngredientRecipes',
                                                       to='recipes.Ingredient',
                                                       verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True,
                                          verbose_name='Название тега')),
                ('color', models.CharField(max_length=7, unique=True,
                                           validators=[
                                               django.core.validators.RegexValidator(
                                                   '^#([a-fA-F0-9]{6})',
                                                   message='Цвет тега должен быть указан в hex формате')],
                                           verbose_name='Цвет Тега')),
                ('slug', models.SlugField(max_length=200, unique=True,
                                          verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('recipe',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='cart', to='recipes.recipe',
                                   verbose_name='Рецепт')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='cart',
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина покупок',
                'verbose_name_plural': 'Корзина покупок',
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='recipes.Tag',
                                         verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipes',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='amount_ingredients', to='recipes.recipe',
                verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('recipe',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='favorites',
                                   to='recipes.recipe',
                                   verbose_name='Рецепт')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='favorites',
                                   to=settings.AUTH_USER_MODEL,
                                   verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ['user'],
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'),
                                               name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipes',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                               name='unique_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'),
                                               name='unique_favourites'),
        ),
    ]
