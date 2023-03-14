from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель для тегов рецептов"""

    name = models.CharField(
        verbose_name="Наименование тега",
        help_text="Имя тега уникально, не может быть пустым, длина 200",
        max_length=200,
        unique=True,
        null=False,
    )
    slug = models.SlugField(
        verbose_name="Slug тега",
        max_length=200,
        unique=True,
        null=True,
    )
    color = models.CharField(
        verbose_name="Цвет тега",
        max_length=7,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингридиентов"""

    name = models.CharField(
        verbose_name="Ингридиент",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единицы измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} {self.measurement_unit}"


class Recipe(models.Model):
    """Модель для рецептов блюд"""

    name = models.CharField(
        verbose_name="Наименование блюда",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Фотография блюда",
    )
    text = models.TextField(
        verbose_name="Описание блюда",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        # related_name="recipes",
        verbose_name="ингридиенты рецепта",
        through="IngredientUnits",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги рецепта",
        related_name="recipes",
        # on_delete=models.CASCADE,
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления",
        null=False,
        validators=[MinValueValidator(1.0)],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации рецепта",
        auto_now_add=True,
        editable=False,
    )


class IngredientUnits(models.Model):
    """Модель связи рецепта и ингридиентов с указанием количества последних"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        # related_name="ingredient",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиенты входящие в рецепт",
        # related_name="recipe",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
    )

    class Meta:
        verbose_name = "Ингридиенты для рецепта"
        verbose_name_plural = "Ингридиенты для рецепта"
        ordering = ("recipe",)

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredient}"


class Favorite(models.Model):
    """Модель избранных рецептов, связь рецепта и пользователя"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Любимый рецепт",
        related_name="favorited",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    time_saved = models.DateTimeField(
        verbose_name="Время сохранения",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favorite_recipe",
            ),
        )
        ordering = ("time_saved",)

    def __str__(self) -> str:
        return (
            f"У пользователя {self.user} избранный/е рецепт/ы: {self.recipe}"
        )


class Cart(models.Model):
    """Модель для списка покупок"""

    pass
