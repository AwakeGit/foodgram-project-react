import csv
import os
import logging

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    DATA_FILE = 'ingredients.csv'

    def import_from_csv_file(self):
        data_file_path = os.path.join(os.path.dirname(os.getcwd()), 'app',
                                      self.DATA_FILE)
        logging.info(f'Importing data from {data_file_path}')

        with open(data_file_path, encoding='utf-8') as data_file:
            data = csv.reader(data_file)
            for data_object in data:
                name, measurement_unit = data_object[:2]

                try:
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                    if created:
                        ingredient.save()
                        logging.info(f'Ingredient "{ingredient}" saved.')
                except Exception as ex:
                    logging.error(f'Error saving ingredient {name}: {str(ex)}')

        self.create_tags()

    def create_tags(self):
        tags = [
            {'name': 'Завтрак', 'slug': 'breakfast', 'color': '#87CEEB'},
            {'name': 'Обед', 'slug': 'lunch', 'color': '#98FF98'},
            {'name': 'Ужин', 'slug': 'dinner', 'color': '#E6E6FA'},
        ]

        for tag_data in tags:
            try:
                Tag.objects.get_or_create(**tag_data)
            except Exception as ex:
                logging.error(
                    f'Error creating tag {tag_data["name"]}: {str(ex)}')

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.import_from_csv_file()
        self.stdout.write(self.style.SUCCESS('Импорт завершен успешно.'))
