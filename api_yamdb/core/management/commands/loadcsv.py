import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db.models.fields import related

from django.conf import settings
from reviews.models import Category, Genre, Title, GenreTitle
from users.models import User


class Command(BaseCommand):
    data_dir = os.path.join(settings.STATICFILES_DIRS[0], 'data')
    help = (
        'Загрузка в базу тестовых данных из файлов .csv в папке '
        f'settings.STATICFILES_DIRS = "{data_dir}"'
    )
    MODELS = {
        Category: {
            'filename': 'category.csv',
            'short': 'c', 'full': 'category'},
        # Comment: {'filename': 'comments.csv', 'short': 'co', 'full': 'comment'},
        Genre: {
            'filename': 'genre.csv',
            'short': 'g', 'full': 'genre'},
        Title: {
            'filename': 'titles.csv',
            'short': 't', 'full': 'title'},
        GenreTitle: {
            'filename': 'genre_title.csv',
            'short': 'gt', 'full': 'genretitle'},
        # Review: {'filename': 'review.csv', 'short': 'r', 'full': 'review'},
        User: {
            'filename': 'users.csv',
            'short': 'u', 'full': 'user'},
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Загрузить данные из всех файлов .csv'
        )
        for model, params in self.MODELS.items():
            full = params['full']
            short = params['short']
            filename = params['filename']
            parser.add_argument(
                f'-{short}',
                f'--{full}',
                action='store_true',
                help=f'Загрузить из "{filename}" в модель "{model.__name__}"'
            )

    def load_csv(self, model, file):
        with open(os.path.join(self.data_dir, file), encoding='utf-8') as f:
            csvreader = csv.DictReader(f)
            objects = []
            for row in csvreader:
                for column, value in row.items():
                    if model == GenreTitle:
                        break
                    field = model._meta.get_field(column)
                    if type(field) == related.ForeignKey:
                        rel_item = field.related_model.objects.get(pk=value)
                        row[column] = rel_item
                objects.append(model(**row))
            model.objects.bulk_create(objects)

    def handle(self, *args, **options):
        need_help = True
        for model, params in self.MODELS.items():
            if model.objects.all().count() > 0:
                self.stdout.write(
                    self.style.NOTICE(
                        f'Модель "{model.__name__}" содержит данные. Если '
                        'будут ошибки, необходимо очистить базу данных и '
                        'повторить загрузку.'
                    )
                )
                # break
            filename = params['filename']
            if options[params['full']] or options['all']:
                need_help = False
                try:
                    self.load_csv(model, filename)
                except Exception as error:
                    raise CommandError(
                        f'Ошибка обработки файла "{filename}" '
                        f'для модели "{model.__name__}"\n{error}'
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Тестовые данные успешно загружены в модель '
                        f'"{model.__name__}"'
                    )
                )
        if need_help:
            self.print_help('manage.py', 'loadcsv')
