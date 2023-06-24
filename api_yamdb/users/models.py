from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    USERNAME_MAX_LENGTH = 150
    EMAIL_MAX_LENGTH = 254

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        'Логин',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')])
    )
    email = models.EmailField(
        'E-mail',
        max_length=EMAIL_MAX_LENGTH,
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
