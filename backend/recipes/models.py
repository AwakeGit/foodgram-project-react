from django.db import models


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=25,
        unique=True,
        help_text='Название тега'
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        default='#000000',
        null=True,
        blank=True,
        unique=True,
        verbose_name='Цвет тега',
        help_text='Цвет тега'
    )
    slug = models.SlugField(
        'Слаг',
        max_length=25,
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_tag'
            )
        ]

    def __str__(self):
        return self.name

