import json

from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('ingredients.json', 'r', encoding='utf-8') as json_file:
            ingredients_data = json.load(json_file)

        for item in ingredients_data:
            name = item.get('name')
            measurement_unit = item.get('measurement_unit')

            ingredient = Ingredient(name=name,
                                    measurement_unit=measurement_unit)
            ingredient.save()

        print('Загрузил!')
