from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import UniqueConstraint
from users.customfields import LowercaseEmailField

class User(AbstractUser):
    """Кастомизированная модель пользователя."""
    email = LowercaseEmailField(
        'Email',
        unique=True,)

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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "password",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name="subscriber",
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="subscribing",
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["id"]
        constraints = [
            UniqueConstraint(
                fields=["user", "author"], name="unique_subscription"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
