import os
import csv
import logging

from django.core.management.base import BaseCommand
from django.db.models.fields import related
from django.conf import settings

from reviews.models import Category, Genre, Title, GenreTitle, Comment, Review
from users.models import User

MSG_NOTFOUND = '{0} - файл не найден!'
MSG_SKIP = '{0}: Пропущено! База данных содержит объекты.'
MSG_SUCCESS = '{0}: Тестовые данные успешно загружены.'
MSG_ERROR = 'Ошибка обработки файла "{0}" для модели "{1}". {2}'

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    data_dir = os.path.join(settings.STATICFILES_DIRS[0], 'data')
    help = (
        'Загрузка в базу тестовых данных из файлов .csv в папке '
        f'settings.STATICFILES_DIRS = "{data_dir}"'
    )
    MODELS = {
        Category: {'filename': 'category.csv', 'short': 'c'},
        Genre: {'filename': 'genre.csv', 'short': 'g'},
        Title: {'filename': 'titles.csv', 'short': 't'},
        GenreTitle: {'filename': 'genre_title.csv', 'short': 'gt'},
        User: {'filename': 'users.csv', 'short': 'u'},
        Review: {'filename': 'review.csv', 'short': 'r'},
        Comment: {'filename': 'comments.csv', 'short': 'co'},
    }

    def __init__(self, *args, **kwargs) -> None:
        """Колоризация логера."""
        logging.addLevelName(
            logging.WARNING,
            "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING)
        )
        logging.addLevelName(
            logging.ERROR,
            "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR)
        )
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        self.args_list = ('all',)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Загрузить данные из всех файлов .csv'
        )
        for model, params in self.MODELS.items():
            full = model._meta.model_name
            short = params['short']
            filename = params['filename']
            parser.add_argument(
                f'-{short}',
                f'--{full}',
                action='store_true',
                help=f'Загрузить из "{filename}" в модель "{model.__name__}"'
            )
            self.args_list += (full,)

    def get_rel_item(self, model, row):
        """Извлечение объектов из связанных моделей."""
        exclude_models = (GenreTitle, Review, Comment)
        exclude_fields = ('genre_id', 'title_id', 'review_id')

        for column, value in row.items():
            if (model in exclude_models and column in exclude_fields):
                continue
            field = model._meta.get_field(column)
            if type(field) == related.ForeignKey:
                rel_item = field.related_model.objects.get(pk=value)
                row[column] = rel_item

    def load_csv(self, model, filename):
        """Загрузка объектов из .csv файла."""
        file = os.path.join(self.data_dir, filename)
        if not os.path.isfile(file):
            raise FileNotFoundError(MSG_NOTFOUND.format(file))

        with open(file, encoding='utf-8') as f:
            csvreader = csv.DictReader(f)
            objects = []
            for row in csvreader:
                self.get_rel_item(model, row)
                objects.append(model(**row))
            model.objects.bulk_create(objects)

    def handle(self, *args, **options):
        if True in (options[key] for key in self.args_list):
            for model, params in self.MODELS.items():
                filename = params['filename']
                if options[model._meta.model_name] or options['all']:
                    if model.objects.all().count() > 0:
                        logger.warning(MSG_SKIP.format(model.__name__))
                        continue
                    try:
                        self.load_csv(model, filename)
                    except Exception as error:
                        logger.error(
                            MSG_ERROR.format(filename, model.__name__, error)
                        )
                    else:
                        logger.info(MSG_SUCCESS.format(model.__name__))
        else:
            self.print_help('manage.py', 'loadcsv')
