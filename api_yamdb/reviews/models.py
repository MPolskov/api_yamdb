from django.db import models
from django.core.validators import RegexValidator


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, validators=[
        RegexValidator(regex='^[-a-zA-Z0-9_]+$')
    ])

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, validators=[
        RegexValidator(regex='^[-a-zA-Z0-9_]+$')
    ])

    def __str__(self):
        return self.name
