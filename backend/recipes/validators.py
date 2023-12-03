import re
from django.core.exceptions import ValidationError


def validate_hex_color(value):
    """
    Проверяет, соответствует ли строка значению цвета формату HEX.
    """
    if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
        raise ValidationError(
            'Введите цвет в формате HEX.'
        )
