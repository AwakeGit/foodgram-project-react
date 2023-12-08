from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet


class NotAllowEmptyForm(BaseInlineFormSet):
    """Форма для удаления ингредиентов или тегов из рецепта."""

    def clean(self):
        """Проверка на наличие ингредиентов или тегов."""
        super().clean()

        counter_true = sum(
            1 for form in self.forms if form.cleaned_data.get('DELETE'))

        if counter_true == len(self.forms):
            raise ValidationError(
                'Нельзя удалить все ингредиенты или теги из рецепта')
