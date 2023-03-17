

{'ingredients': [{'id': 1,'amount': 10}],'tags': [1, 2],'name': '12','text': '12','cooking_time': 1}


from api.serializers import RecipeSerializerWrite

serializer = RecipeSerializerWrite(data={'ingredients': [{'id': 1,'amount': 10}],'tags': [1, 2],'name': '12','text': '12','cooking_time': 1})

serializer
RecipeSerializerWrite(
    data={'ingredients': [{'id': 1, 'amount': 10}], 'tags': [1, 2], 'name': '12', 'text': '12', 'cooking_time': 1}):
    
    id = IntegerField(label='ID', read_only=True)
    tags = PrimaryKeyRelatedField(allow_empty=False, label='Теги рецепта', many=True, queryset=Tag.objects.all())
    ingredients = PrimaryKeyRelatedField(label='Ингридиенты рецепта', many=True, read_only=True)
    name = CharField(label='Наименование блюда', max_length=200)
    text = CharField(label='Описание блюда', style={'base_template': 'textarea.html'})
    cooking_time = IntegerField(label='Время приготовления', min_value=1.0)


{
  "username": "pupkin",
  "password": "admin123!",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "email": "vpupkin@yandex.ru"
}