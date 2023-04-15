# Generated by Django 4.1.7 on 2023-03-16 20:21

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=150, verbose_name="Пароль"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "Пользователь уже существует"},
                help_text="Обязательно. Максимум 150 символов. Буквы, цифры и @/./+/-/_.",
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name="Уникальный юзернейм",
            ),
        ),
    ]