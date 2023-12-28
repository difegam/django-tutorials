# Poetry

## Setup poetry

1. Install poetry

To install poetry please follow the instructions on the [poetry website](https://python-poetry.org/docs/#installing-with-the-official-installer)

2. Create a `poetry.toml` file in the project directory

```config
[virtualenvs]
in-project = true
```

```shell
echo -e "[virtualenvs]\nin-project = true" > poetry.md
```

## Start a Django project using poetry

Create a new project directory

```shell
poetry new project_name
```

Update pip to the latest version

```shell
poetry run python -m pip install --upgrade pip
```

Add django and python-dotenv to the project

```shell
poetry add django@4.1 python-dotenv
```

Add development dependencies

- Pytest
- djlint

```shell
poetry add djlint pytest@7.4 -D
```

Create a new django project in the current directory

```shell
poetry run django-admin startproject project_name .
```

## Start a Django app using poetry

```shell
poetry run py manage.py startapp app_name
```

## Run Django server

```shell
poetry run python manage.py runserver
```
