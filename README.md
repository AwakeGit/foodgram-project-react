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
cd foodgram-project-react
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
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml exec backend python manage.py makemigrations   
docker-compose -f docker-compose.yml exec backend python manage.py migrate
docker-compose -f docker-compose.yml exec backend python manage.py collectstatic --noinput
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
КОМАНДЫ для загрзки данных
```