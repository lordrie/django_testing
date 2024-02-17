# Django Testing  

## Описание проекта

"Django Testing" - это проект, посвященный тестированию проектов YaNote и YaNews с использованием unittest и pytest.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lordrie/django_testing
```

Cоздать и активировать виртуальное окружение:

```
cd django_testing-main/
```
```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект ya_news с pytest:
```
./run_tests.sh
```
Запустить проект ya_note с unittest:
```
cd ya_note/
python manage.py test
```
