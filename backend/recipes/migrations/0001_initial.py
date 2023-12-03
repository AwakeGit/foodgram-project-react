# Generated by Django 2.2.19 on 2023-12-03 13:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название нового ингредиента (не более 200 символов)', max_length=200, verbose_name='название')),
                ('measurement_unit', models.CharField(help_text='Введите подходящие единицы измерения для нового ингредиента', max_length=200, verbose_name='единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Задайте требуемое количество для выбранного ингредиента', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32767)], verbose_name='количество')),
                ('ingredient', models.ForeignKey(help_text='Выберете ингредиент из предложенного перечня', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.Ingredient', verbose_name='ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название блюда (название рецепта)', max_length=200, unique=True, verbose_name='название')),
                ('image', models.ImageField(help_text='Укажите ссылку на картинку в Base64: Например: data:image/png;base64,iVBORw0KGgo...', upload_to='recipes/images/', verbose_name='картинка блюда')),
                ('text', models.TextField(help_text='Введите текст рецепта', verbose_name='описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Укажите время приготовления блюда', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(32767)], verbose_name='время приготовления (в минутах)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')),
                ('author', models.ForeignKey(help_text='Выберете автора рецепта из предложенного перечня', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор рецепта')),
                ('ingredients', models.ManyToManyField(help_text='Выберете ингредиенты в требуемом количестве.', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='список ингредиентов')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название нового тега (не более 200 символов)', max_length=200, unique=True, verbose_name='название')),
                ('color', models.CharField(help_text='Укажите цвет для тега в формате HEX (не более 7 символов, включая знак "#"). Например "#E26C2D"', max_length=7, unique=True, validators=[recipes.models.validate_hex_color], verbose_name='цвет в HEX')),
                ('slug', models.SlugField(help_text='Введите уникальный слаг - строку, максимальной длиной не более 200 символов, состоящую из букв, цифр, дефиса и знака подчёркивания', max_length=200, unique=True, verbose_name='уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Выберете рецепт, добавляемый в список покупок', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to='recipes.Recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(help_text='Выберете пользователя, который добавляет тот или иной рецепт в список покупок', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_lists', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберете нужные теги.', related_name='recipes', to='recipes.Tag', verbose_name='список тегов'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Выберете рецепт из предложенного перечня!', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_in_recipe', to='recipes.Recipe', verbose_name='рецепт'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Выберете рецепт, добавляемый в избранное', on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='recipes.Recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(help_text='Выберете пользователя, который добавляет тот или иной рецепт в избранное', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user-recipe-shoppinglist constraint'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='ingredient-recipe constraint'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user-recipe constraint'),
        ),
    ]
