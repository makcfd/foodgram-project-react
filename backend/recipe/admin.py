from django.contrib import admin
from recipe.models import Tag, Recipe, Ingredient

# Register your models here.
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
