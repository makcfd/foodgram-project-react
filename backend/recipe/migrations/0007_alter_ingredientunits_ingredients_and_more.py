# Generated by Django 4.1.7 on 2023-03-13 20:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0006_remove_recipe_tags_recipe_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientunits",
            name="ingredients",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipe.ingredient",
                verbose_name="Ингредиенты входящие в рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="ingredientunits",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="recipe.recipe",
                verbose_name="Рецепт",
            ),
        ),
        migrations.AlterField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipe.IngredientUnits",
                to="recipe.ingredient",
                verbose_name="ингридиенты рецепта",
            ),
        ),
    ]
