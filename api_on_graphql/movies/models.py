from django.db import models


class Actor(models.Model):
    """Актёр."""
    name = models.CharField('Имя', max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    """Фильм."""
    title = models.CharField('Название', max_length=100)
    actors = models.ManyToManyField(
        Actor,
        verbose_name='актёры',
        related_name='movies'
    )
    year = models.PositiveIntegerField('год_премьеры')

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self) -> str:
        return self.name
