# praktikum_new_diplom

### Логин awake

### Пароль qwesadzxc123

docker system prune -af
docker compose -f docker-compose.yml pull
docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml exec backend python manage.py makemigrations
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/
docker compose -f docker-compose.yml exec backend python manage.py load_csv
docker compose -f docker-compose.yml exec backend python manage.py
import_ingredients
docker-compose exec backend python manage.py data_test
docker compose -f docker-compose.yml exec backend python manage.py data_test