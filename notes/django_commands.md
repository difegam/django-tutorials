# Django Commands

## Run Development Server

```bash
poetry run python manage.py runserver
```

## Create superuser:

```bash title="Create superuser"
poetry run python manage.py createsuperuser
```

## Shell

```bash
poetry run python manage.py shell
```

## Migrations

```bash
poetry run python manage.py makemigrations
```

```bash
poetry run python manage.py migrate
```

```bash
poetry run python manage.py showmigrations
```

## Dumping the existing data
The dumpdata command dumps data from the database into the standard output, serialized in JSON format by default. Django supports fixtures in JSON, XML, or YAML formats.

```bash
poetry run python manage.py dumpdata --indent=2 --output=mysite_data.json
```

## Loading the data from the dump
The loaddata command loads data from the serialized data file into the database.

```bash
poetry runpython manage.py loaddata mysite_data.json
```