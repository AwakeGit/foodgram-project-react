#!/bin/bash

# Удалить все неиспользуемые ресурсы Docker
#docker system prune -af

# Обновить образы, указанные в docker-compose.yml
docker-compose -f docker-compose.yml pull

# Остановить и удалить контейнеры, запущенные из docker-compose.yml
docker-compose -f docker-compose.yml down

# Пересобрать и перезапустить контейнеры
docker-compose -f docker-compose.yml up -d --build

# Выполнить миграции базы данных
docker-compose -f docker-compose.yml exec backend python manage.py makemigrations users
docker-compose -f docker-compose.yml exec backend python manage.py makemigrations recipes

docker-compose -f docker-compose.yml exec backend python manage.py migrate

# Собрать статические файлы
docker-compose -f docker-compose.yml exec backend python manage.py collectstatic --noinput

# Копировать собранные статические файлы в указанную директорию
docker-compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/

# Импортировать ингредиенты
docker-compose -f docker-compose.yml exec backend python manage.py load_data