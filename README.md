# FoodGram

### Данные для входа

```bash 
admin
admin@gmail.com
qwesadzxc123

user@gmail.com
user
qwesadzxc123

https://taski-awake.ddns.net/
````

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
docker-compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/
docker-compose -f docker-compose.yml exec backend python manage.py load_data
```

## Использование в реальной среде

1. Подключиться к серверу:
```bash
ssh -i [name] [user]@[ip]
```
2. Создать и перейти в каталог проекта:
```bash
mkdir foodgram
cd foodgram
```
3. Создать .env файл и docker-compose.production.yml:
4. Запустить проект в докере:
```bash
sudo docker system prune -af
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d --build
sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_data
```