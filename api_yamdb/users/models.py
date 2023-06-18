from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')])
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=40,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
