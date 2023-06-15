from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
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

    def __str__(self):
        return self.username
