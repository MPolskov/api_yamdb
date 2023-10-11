# Проект YaMDb
Учебный групповой проект по API (Django REST framework).

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся.

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## Установка и запуск проекта:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:MPolskov/api_yamdb.git
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
py -3.9 -m venv venv
```
```
source ./venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install -r requirements.txt
```
Выполнить миграции:
```
python api_yamdb/manage.py migrate
```
Запустить сервер:
```
python api_yamdb/manage.py runserver 0.0.0.0:8000
```

## Импорт тестовых данных
Тестовые данные для базы данных проекта расположены в папке /static.

### Утилита загрузки данных интегрирована в manage.py
Параметры командной строки
```
$ python api_yamdb/manage.py loadcsv
usage: manage.py loadcsv [-h] [-a] [-c] [-g] [-t] [-gt] [-u] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color] [--skip-checks]

Загрузка в базу тестовых данных из файлов .csv в папке settings.STATICFILES_DIRS = "D:\edu\api_yamdb\api_yamdb\static\data"

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Загрузить данные из всех файлов .csv
  -c, --category        Загрузить из "category.csv" в модель "Category"
  -g, --genre           Загрузить из "genre.csv" в модель "Genre"
  -t, --title           Загрузить из "titles.csv" в модель "Title"
  -gt, --genretitle     Загрузить из "genre_title.csv" в модель "GenreTitle"
  -u, --user            Загрузить из "users.csv" в модель "User"
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g. "myproject.settings.main". If this isn't provided, the DJANGO_SETTINGS_MODULE environment variable will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.
  --skip-checks         Skip system checks.
```
Пример импорта:
```
$ python api_yamdb/manage.py loadcsv -a
Category: Тестовые данные успешно загружены.
Genre: Тестовые данные успешно загружены.
Title: Тестовые данные успешно загружены.
GenreTitle: Тестовые данные успешно загружены.
User: Тестовые данные успешно загружены.
```
## Авторы:
### Полшков Михаил
Реализация части проекта, касающейся управления пользователями:
- система регистрации и аутентификации;
- права доступа;
- работа с токеном;
- система подтверждения через e-mail.
### Папулов Евгений
- реализация моделей, view и эндпойнтов для произведений, категорий, жанров;
- реализация импорта данных из csv файлов.
### Минниев Айрат
- реализация моделей, view и эндпойнтов для отзывов, комментариев, рейтинга произведений.
