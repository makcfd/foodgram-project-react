import csv
from django.core.management.base import BaseCommand, CommandError
from recipe.models import Ingredient


class Command(BaseCommand):
    help = """Загружает из csv файла данные в модели DRF.
    Argument to call command
    ------------------------
    --docname : str
        ingredients
    """

    DEFAULT_PATH_TO_DATA = (
        "/Users/fedius/Documents/Dev/foodgram-project-react/data/"
    )

    def add_arguments(self, parser):
        parser.add_argument("--docname", type=str)

    def _category_bulk_create(self, reader):
        bulk_list = list()
        for row in reader:
            print(row)
            bulk_list.append(Ingredient(name=row[0], measurement_unit=row[1]))
        try:
            Ingredient.objects.bulk_create(bulk_list)
        except Exception as error:
            raise CommandError(
                "При наполении таблицы категорий возникла ошибка", error
            )
        return len(bulk_list)

    def handle(self, *args, **options):
        docname = options["docname"]
        if self.DEFAULT_PATH_TO_DATA is None:
            path = docname + ".csv"
        else:
            path = self.DEFAULT_PATH_TO_DATA + docname + ".csv"
        with open(path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            num_objects = self._category_bulk_create(reader=reader)

        self.stdout.write(
            self.style.SUCCESS(f"Успешно загруженно объектов: {num_objects}")
        )
