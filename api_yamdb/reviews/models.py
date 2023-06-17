import datetime
from django.db import models
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator
)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class BaseModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        abstract = True

    def to_dict(self):
        return {'slug': self.slug, 'name': self.name}

    def __str__(self):
        return self.name


class Category(BaseModel):
    pass


class Genre(BaseModel):
    pass


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[
            MinValueValidator(limit_value=1900),
            MaxValueValidator(limit_value=current_year())
        ],
    )
    rating = models.IntegerField(verbose_name='Рейтинг', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              on_delete=models.CASCADE,
                              related_name='titles')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='genres')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['genre', 'title'],
                                    name='unique_follow')
        ]

    def __str__(self):
        return f'{self.genre} {self.title}'
