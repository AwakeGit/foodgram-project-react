Как можно улучшить READMD:

# FoodGram

## Описание

Фудграм представляет собой веб-приложение, созданное для
любителей кулинарии, где пользователи могут делиться своими рецептами,
добавлять чужие блюда в избранное и подписываться на публикации других авторов.
Помимо этого, сервис предоставляет удобный инструмент "Список покупок", который
позволяет создавать персональные списки продуктов для приготовления выбранных
блюд.

## Возможности приложения:

**Публикация Рецептов:** Пользователи могут делиться своими кулинарными
шедеврами,
публикуя рецепты с подробным описанием и фотографиями.

**Избранное и Подписки:** Возможность добавлять любимые рецепты в избранное и
подписываться на авторов для получения обновлений.

**Список Покупок:** Удобный сервис для создания списка продуктов, необходимых
для
приготовления выбранных блюд.

**Выгрузка в Файл (.txt):** Возможность экспорта списка продуктов в текстовый
файл
для удобства покупок.

## Локальное использование

1. Склонировать репозиторий:

```bash
git clone git@github.com:AwakeGit/foodgram-project-react.git
```

2. Перейти в каталог проекта:

```bash
cd foodgram-project-react/infra
```

3. Создать .env файл:

```bash
SECRET_KEY='secret_key'

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=foodgram_db
POSTGRES_USER=foodgram_db_user
POSTGRES_PASSWORD=foodgram_db_password

DB_HOST=db
DB_PORT=5432
```

4. Запустить проект в докере:

```bash
docker system prune -af
docker compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
docker-compose exec backend python manage.py import_tags
docker-compose exec backend python manage.py import_ingredients
docker-compose exec backend python manage.py data_test
```