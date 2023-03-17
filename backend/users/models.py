from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    """Кастомизированная модель пользователя."""

    first_name = models.CharField(
        verbose_name="Имя", max_length=150, blank=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=150, blank=False
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="Уникальный юзернейм",
        max_length=150,
        unique=True,
        help_text="Обязательно. Максимум 150 символов. Буквы, цифры и @/./+/-/_.",
        validators=[username_validator],
        error_messages={
            "unique": "Пользователь уже существует",
        },
    )

    # password = models.CharField(verbose_name="Пароль", max_length=150)

    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "email",
        "password",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
